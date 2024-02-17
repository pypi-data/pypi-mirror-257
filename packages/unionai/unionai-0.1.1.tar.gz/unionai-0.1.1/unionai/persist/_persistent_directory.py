import logging
import os
import sys
import typing
from pathlib import Path
from time import sleep

POD_MOUNT_PATH = "/nodecache"

_DEFAULT_LOGGER = logging.getLogger("persist")
_DEFAULT_LOGGER.setLevel(logging.INFO)
_DEFAULT_LOGGER.addHandler(logging.StreamHandler(sys.stdout))

T = typing.TypeVar("T")


class PersistentDirectory(os.PathLike, typing.Generic[T]):
    def __init__(self, path: Path = POD_MOUNT_PATH, logger: logging.Logger = _DEFAULT_LOGGER, *args, **kwargs):
        self.path = path
        self.warm = False
        self._logger = logger

    def check(self, timeout=600) -> Path:
        elapsed = 0
        pause = 5
        while ".done" not in os.listdir(self.path) and elapsed < timeout:
            self._logger.debug(f"Sleeping for {pause} seconds while cache is populated...")
            sleep(pause)
            elapsed += pause
        if elapsed >= timeout:
            raise TimeoutError(f"Populating cache timed out after {timeout} seconds.")
        self.warm = True
        return self.__fspath__()

    def __fspath__(self):
        return str(self.path)

    def __repr__(self) -> str:
        if not self.warm:
            self.check()
        return str(self.path)

    def __str__(self) -> str:
        return str(self.path)
