"""Repo on fire main application."""

import json
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from typing import List, Optional

from .configuration import Configuration, get_user_config_file_path, load_configuration
from .exceptions import RepoOnFireException
from .repo import Repo


class Application:
    """The repo-on-fire application."""

    def __init__(self, configuration: Optional[Configuration] = None) -> None:
        """Create a new instance of the app.

        Args:
            configuration: The configuration to use. If not given, load from
                           default settings files.
        """
        if configuration is not None:
            self._configuration = configuration
        else:
            self._configuration = load_configuration()
        self._repo = Repo(self._configuration)

    def run_command_line(self, args: Optional[List[str]] = None):
        """Run the command line interface."""
        if args is None:
            args = sys.argv[1:]

        parser = self._create_arg_parser()
        values, unparsed = parser.parse_known_args(args=args)

        if "func" in values:
            if values.help:
                unparsed.append("--help")
            values.func(args, values, unparsed)
        else:
            parser.print_help()

    def _create_arg_parser(self) -> ArgumentParser:
        """Create the argument parser.

        This creates a new ArgumentParser, which is used to extract some
        information from commands we wrap around and - on top - some
        custom parsing logic for repo-on-fire specific functionality.
        """
        parser = ArgumentParser(
            description="Wrapper around Google's repo tool",
            formatter_class=ArgumentDefaultsHelpFormatter,
            add_help=False,
        )
        parser.add_argument("--help", "-h", action="store_true", help="Show the built in help.")
        sub_parsers = parser.add_subparsers()

        # Add known repo commands:
        self._add_known_repo_commands(sub_parsers)

        # Add own commands
        config_cmd = sub_parsers.add_parser(
            "config", help="Interact with repo-on-fires configuration."
        )
        self._init_config_commands(config_cmd)

        return parser

    def _add_known_repo_commands(self, subparsers):
        """Add the known repo commands to the CLI."""
        # Add the known repo commands. Depending on the concrete command,
        # we either pass through as-is or add some magic on top:
        known_repo_commands = self._repo.get_known_repo_commands()
        for known_repo_command in known_repo_commands:
            command = subparsers.add_parser(
                known_repo_command.command, add_help=False, help=known_repo_command.description
            )
            if known_repo_command.command == "init":
                command.add_argument("-u", "--manifest-url", type=str)
                command.add_argument("-m", "--manifest-name", type=str)
                command.add_argument("--mirror", action="store_true")
                command.add_argument("--reference", type=str)
                command.set_defaults(func=self._run_decorated_init)
            else:
                command.set_defaults(func=self._run_repo_pass_through_args)

    def _init_config_commands(self, config_command: ArgumentParser):
        """Set up sub-commands of the config command."""
        config_command.set_defaults(func=lambda *args: config_command.print_help())
        sub_parsers = config_command.add_subparsers(title="Configuration")

        path_command = sub_parsers.add_parser(
            "path", help="Print path to the used configuration files."
        )
        path_command.set_defaults(func=self._run_command_config_path)
        path_command.add_argument("--json", help="Print as JSON", action="store_true")

        list_command = sub_parsers.add_parser("list", help="Show the used configuration.")
        list_command.set_defaults(func=self._run_command_config_list)
        list_command.add_argument("--json", help="Print as JSON", action="store_true")

    def _run_repo_pass_through_args(self, args, *other_args):
        """Call repo, passing through any arguments as-is."""
        # Invoke repo with any arguments passed-through as-is:
        sys.exit(self._repo.call(args))

    def _run_decorated_init(self, args: List[str], values, unparsed: List[str]):
        """Run the repo init command.

        This runs the init command of repo, potentially with some extras
        on top, as needed.

        Args:
            args: The list of original arguments - as it.
            values: The list of parsed values.
            unparsed: The list of parsed values not consumed by us.
        """
        # If the user uses any of --mirror or --reference (i.e. the typical
        # options that are used when caching!) don't bother and pass-through as
        # is! We don't want to interfere here.
        # Also, if no URL is given, also pass-through.
        if values.mirror or values.reference is not None or values.manifest_url is None:
            self._run_repo_pass_through_args(args)
            return

        # If the used tried to run an init with a valid URL, do the following:
        # 1. Create or update a mirror.
        # 2. Create the actual workspace using repo init.
        self._repo.create_or_update_cache_entry(values.manifest_url, values.manifest_name)
        self._repo.init_from_cache_entry(values.manifest_url, values.manifest_name, unparsed)

    def _run_command_config_path(self, _, values, unparsed: List[str]):
        """Print the path to the configuration file."""
        if len(unparsed) > 0:
            raise RepoOnFireException(f"Unexpected arguments given: {unparsed}")
        if values.json:
            data = {"path": str(get_user_config_file_path())}
            print(json.dumps(data, indent="  "))
        else:
            print(get_user_config_file_path())

    def _run_command_config_list(self, _, values, unparsed: List[str]):
        """Print the configuration settings used by the app."""
        if len(unparsed) > 0:
            raise RepoOnFireException(f"Unexpected arguments given: {unparsed}")
        if values.json:
            print(self._configuration.model_dump_json(indent=2))
        else:
            config_dict = self._configuration.model_dump()
            for key, value in config_dict.items():
                print(f"{key} = {value}")
