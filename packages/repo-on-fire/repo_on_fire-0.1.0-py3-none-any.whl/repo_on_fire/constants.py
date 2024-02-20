"""Constant definitions."""

from enum import Enum

APP_NAME = "RepoOnFire"
"""The name of the app (as used e.g. in file paths)."""

APP_AUTHOR = "RPdev"
"""The app's author (as used e.g. in file paths)."""

CONFIG_FILE_NAME = "config.env"
"""The file name of the settings file."""

CACHE_ENTRY_STAMP_FILE = ".repo-on-fire-stamp"
"""The name of the stamp file stored in cached workspaces."""


class WorkspaceCacheStrategy(str, Enum):
    """The strategy to use for workspace cache handling."""

    auto_sync = "auto_sync"
    """Automatically cache workspaces.

    With this strategy, when a new workspace is initialized, a mirror workspace
    in the cache will be created and the new workspace will use it as a
    reference. If the mirror workspace already exists, it will be kept up to
    date whenever new workspaces are created.
    """

    auto_sync_dissociate = "auto_sync_dissociate"
    """Automatically cache workspaces but remove association to cache.

    This strategy is similar to `auto_sync`, however, the newly created
    workspace will be dissociated from the cache entry after initial sync.
    """
