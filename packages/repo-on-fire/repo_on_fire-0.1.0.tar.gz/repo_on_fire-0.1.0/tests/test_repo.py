"""Test the repo wrapper."""

from pathlib import Path
from tempfile import TemporaryDirectory

from repo_on_fire.configuration import Configuration
from repo_on_fire.repo import Repo


def test_repo():
    """Check that the simple repo wrapper works.

    We expect it to let us fetch repo and call it easily on the command line.
    """
    with TemporaryDirectory() as tmp_dir:
        configuration = Configuration(cache_path=Path(tmp_dir))
        repo = Repo(configuration=configuration)
        repo.call(["init", "--help"])
        repo.call(["--help"])
