"""Define functions to interact with the file system.

Created: 04.10.2023
@author: Max Weise
"""

import pathlib
import subprocess

import pystrap.system_core

# === Type definition
pathlike = pathlib.Path | str


# === IO Operations
def create_folder(path_to_folder: pathlib.Path) -> bool:
    """Create a folder.

    Args:
        path_to_folder: The path to the folder, relative to the current
            working directory.

    Returns:
        bool: Sucessvalue of the function.

    Raises:
        FileExistsError: When the given directory already exists.
    """
    if path_to_folder.exists():
        raise FileExistsError

    subprocess.run(["mkdir", "-p", path_to_folder])

    return True


def create_file(path_to_file: pathlib.Path) -> bool:
    """Create a file.

    Args:
        path_to_file: The path to the file, relative to the current
            working directory.

    Returns:
        bool: The sucessvalue of the function.

    Raises:
        FileExistsError: When the given filepath already exists.
    """
    if path_to_file.exists():
        raise FileExistsError

    subprocess.run(["touch", path_to_file])

    return True


def _file_is_empty(path_to_file: pathlike) -> bool:
    with open(path_to_file, "r", encoding="utf-8") as f:
        file_contents: list[str] = f.readlines()
        if file_contents:
            return False

    return True


def write_contents_to_file(
    path_to_file: pathlike,
    contents: str,
) -> bool:
    """Write a string to an already existing file.

    Args:
        path_to_file: The file which is written to.
        contents: The contents of the file as strings.

    Returns:
        bool: Sucessvalue of the method.

    Raises:
        FileNotEmptyException: Gets raised when trying to write to
            a non-empty file.
    """
    if not _file_is_empty(path_to_file):
        raise pystrap.system_core.FileNotEmptyException(
            "Can't write to a non-empty file!"
        )

    with open(path_to_file, "w", encoding="utf-8") as f:
        f.write(contents)

    return True
