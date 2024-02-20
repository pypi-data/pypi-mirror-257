"""Test the configuration module."""

from repo_on_fire.configuration import Configuration


def test_configuration_constructor():
    """Test if we can create a Configuration object."""
    config = Configuration()
    assert config is not None
