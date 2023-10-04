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
def create_folder(
    path_to_folder: pathlike,
    logger: pystrap.system_core.Logger
) -> bool:
    """Create a folder.

    Args:
        path_to_folder: The path to the folder, relative to the current
            working directory.

    Returns:
        bool: Sucessvalue of the function.
    """
    logger.info(f"Creating the folder {path_to_folder}")
    subprocess.run(["mkdir", "-p", path_to_folder])

    return True


def create_file(
    path_to_file: pathlike,
    logger: pystrap.system_core.Logger
) -> bool:
    """Create a file.

    Args:
        path_to_file: The path to the file, relative to the current
            working directory.

    Returns:
        bool: The sucessvalue of the function.
    """
    logger.info(f"Creating the file {path_to_file}")
    subprocess.run(["touch", path_to_file])

    return True


def write_contents_to_file(
    path_to_file: pathlike,
    contents: str,
    logger: pystrap.system_core.Logger
) -> bool:
    """Write a string to an already existing file.

    Args:
        path_to_file: The file which is written to.
        contents: The contents of the file as strings.

    Returns:
        bool: Sucessvalue of the method.
    """
    logger.info(f"Writing to {path_to_file}")
    with open(path_to_file, "w", encoding="utf-8") as f:
        f.write(contents)

    return True
