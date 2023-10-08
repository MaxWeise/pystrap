"""Define functions that collect configuration data for fresh projects.

Created: 04.10.2023
@author: Max Weise
"""

import pathlib
from typing import Any

import tomli_w

import pystrap.io_operations
import pystrap.system_core

# === Type definition
pathlike = pathlib.Path | str


# === Usecase specific functions
def create_project_structure(
    project_name: str,
    logger: pystrap.system_core.Logger,
    distributable: bool = False
) -> bool:
    """Create all necessary folders and configuration files.

    Args:
        project_name: The name of the project.

    Return:
        bool: Sucessvalue of the function.
    """
    toplevel_file_names = ["pyproject.toml"]

    if distributable:
        toplevel_file_names.append("setup.py")

    project_folders = [f"src/{project_name}", "tests"]
    init_files = ["tests/__init__.py", f"src/{project_name}/__init__.py"]

    logger.info("Creating folders")
    for folder_name in project_folders:
        try:
            pystrap.io_operations.create_folder(pathlib.Path(folder_name))
        except FileExistsError:
            logger.warning(f"The folder {folder_name} already exists.")

    logger.info("Creating files")
    for file_name in toplevel_file_names:
        try:
            pystrap.io_operations.create_file(pathlib.Path(file_name))
        except FileExistsError:
            logger.warning(f"The file {file_name} already exists.")

    logger.info("Creating init-files")
    for init_file in init_files:
        try:
            pystrap.io_operations.create_file(pathlib.Path(init_file))
        except FileExistsError:
            logger.warning(f"The file {init_file} already exists.")

    return True


def get_project_metadata(
    project_name: str,
    description: str | None = None,
    author: pystrap.system_core.Author | None = None
) -> dict[str, Any]:
    """Get the metadata for the pyproject.toml file.

    Args:
        project_name (str): The name of the created project.
        description (str): Short description of the created project.
        author (Author): The name and email adress of the author.

    Returns
        project_metadata (dict[str, Any]): The metadata of the created project.
    """
    project_metadata: dict[str, Any] = {}

    author_name: str = author.name if author else ""
    author_email: str = author.email if author else ""
    project_description: str = description if description else ""
    authors: dict[str, str] = {
        "name": author_name,
        "email": author_email
    }

    project: dict[str, Any] = {
        "name": project_name,
        "description": project_description,
        "version": "0.0.1",
        "authors": [authors],
        "maintainers": [authors],
        "requires-python": ">=3.10"
    }

    project_metadata["project"] = project

    return project_metadata


def get_build_system_config() -> dict[str, Any]:
    """Get the standart configuration for the build system.

    Returns:
        build_system_config (dict[str, Any]): A dictionary containing default
            settings for a <build-system> section in a pyproject.toml file.
    """
    build_system_config: dict[str, Any] = {
        "[build-system]": {
            "requires": [
                "setuptools>=42",
                "wheel"
            ],
            "build-backend": "setuptools.build_meta"
        }
    }

    return build_system_config


def write_configuration_to_files(
    project_name: str,
    logger: pystrap.system_core.Logger,
    distributable: bool = False,
    author: pystrap.system_core.Author | None = None,
    description: str | None = None
) -> bool:
    """Write configuration data to the configuration files.

    Args:
        project_name: The name of the product.
    """
    if not description:
        description = "This project has been created with pystrap."

    logger.info("Writing contents to files")
    pyprojcect_contents: dict[str, Any] = get_project_metadata(
        project_name,
        author=author,
        description=description
    )
    path_to_pyproject_file: pathlib.Path = pathlib.Path("pyproject.toml")
    try:
        pystrap.io_operations.write_contents_to_file(
            path_to_pyproject_file,
            tomli_w.dumps(pyprojcect_contents)
        )
    except pystrap.system_core.FileNotEmptyException:
        logger.warning(
            f"The file {path_to_pyproject_file} is not empty. "
            "Can't write to a non-empty file!"
        )

    if distributable:
        setup_py_contents = (
            "from setuptools import setup"
            "\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    setup()"
        )
        path_to_setup_file: pathlib.Path = pathlib.Path("setup.py")
        try:
            pystrap.io_operations.write_contents_to_file(
                path_to_setup_file,
                setup_py_contents
            )
        except pystrap.system_core.FileNotEmptyException:
            logger.warning(
                f"The file {path_to_pyproject_file} is not empty. "
                "Can't write to a non-empty file!"
            )

    return True
