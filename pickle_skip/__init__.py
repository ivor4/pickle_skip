import os

from pickle_skip import ContainerObject
from pickle_skip import PickleSkipper

# Read version from file
version_file = os.path.join(os.path.dirname(__file__), "version.txt")
with open(version_file) as file_handler:
    __version__ = file_handler.read().strip()



__all__ = [
    "ContainerObject",
    "PickleSkipper",
]
