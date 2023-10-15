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


# === Functions get sorted by what file they create
def create_pyprojecttoml_file(
    project_name: str,
    author: pystrap.system_core.Author,
    logger: pystrap.system_core.Logger,
    file_name: pathlike = "pyproject.toml"
) -> bool:
    """Create the pyproject.toml file.

    Use the argument [file_name] in testing and set it to something different
    than the standard name. This ensures that the original pyproject file is
    not acidentally removed when executing automated tests.

    Args:
        project_name (str): The name of the prject.
        author (Author): The authors name and email adress.
        logger: The logger object handeling log statements.
        file_name (pathlike, optional): Change the name when automatically
            testing the function. Defaults to pyproject.toml.
    """
    logger.info("Creating pyproject.toml file.")
    try:
        if isinstance(file_name, str):
            file_name = pathlib.Path(file_name)

        pystrap.io_operations.create_file(file_name)
    except FileExistsError:
        logger.warning(f"The file {file_name} already exists.")

    project_metadata: dict[str, Any] = {}
    section_project: dict[str, Any] = {
        "name": project_name,
        "version": "0.0.1",
        "authors": author.to_list(),
        "maintainers": author.to_list(),
        "requires-python": ">=3.10"
    }
    section_buildsytem = {
        "requires": [
            "setuptools>=42",
            "wheel"
        ],
        "build-backend": "setuptools.build_meta"
    }
    project_metadata["project"] = section_project
    project_metadata["build-system"] = section_buildsytem

    pystrap.io_operations.write_contents_to_file(
        file_name,
        tomli_w.dumps(project_metadata),
    )

    return True


def create_setuppy_file(
    logger: pystrap.system_core.Logger,
    file_name: pathlike = "setup.py"
) -> bool:
    """Create the setup.py file.

    Use the argument [file_name] in testing and set it to something different
    than the standard name. This ensures that the original setup file is not
    acidentally removed when executing automated tests.

    Args:
        project_name (str): The name of the prject.
        author (Author): The authors name and email adress.
        logger: The logger object handeling log statements.
        file_name (pathlike, optional): Change the name when automatically
            testing the function. Defaults to pyproject.toml.
    """
    logger.info("Creating setup.py file.")
    try:
        if isinstance(file_name, str):
            file_name = pathlib.Path(file_name)

        pystrap.io_operations.create_file(file_name)
    except FileExistsError:
        logger.warning(f"The file {file_name} already exists.")

    setup_py_contents = (
        "from setuptools import setup"
        "\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    setup()"
    )
    pystrap.io_operations.write_contents_to_file(
        pathlib.Path(file_name),
        setup_py_contents,
    )

    return True


# === Usecase specific functions
def create_project_structure(
    project_name: str,
    logger: pystrap.system_core.Logger,
) -> bool:
    """Create all necessary folders and configuration files.

    Args:
        project_name: The name of the project.

    Return:
        bool: Sucessvalue of the function.
    """
    project_folders = [f"src/{project_name}", "tests"]
    init_files = ["tests/__init__.py", f"src/{project_name}/__init__.py"]

    logger.info("Creating folders")
    for folder_name in project_folders:
        try:
            pystrap.io_operations.create_folder(pathlib.Path(folder_name))
        except FileExistsError:
            logger.warning(f"The folder {folder_name} already exists.")

    logger.info("Creating init-files")
    for init_file in init_files:
        try:
            pystrap.io_operations.create_file(pathlib.Path(init_file))
        except FileExistsError:
            logger.warning(f"The file {init_file} already exists.")

    return True
