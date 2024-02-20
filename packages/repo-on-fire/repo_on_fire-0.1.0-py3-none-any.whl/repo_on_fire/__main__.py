"""Entry points for console."""

from .application import Application


def main():
    """Main entry point."""
    app = Application()
    app.run_command_line()


if __name__ == "__main__":
    main()
