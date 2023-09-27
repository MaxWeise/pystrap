"""Main method for the python-bootstrap skript.

Created: 22.08.2023
@author: Max Weise
"""

import argparse
import dataclasses
import logging
import pathlib
import subprocess
from typing import Any, Protocol

import tomli_w

# === Type definition
pathlike = pathlib.Path | str


class Logger(Protocol):
    """Logger interface all loggers used must adhere to."""

    def info(self, message: str) -> None:
        """Print an info message to the screen.

        Args:
            message (str): The message printed to the screen.
        """
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )

    def warning(self, message: str) -> None:
        """Print an warning message to the screen.

        Args:
            message (str): The message printed to the screen.
        """
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )

    def error(self, message: str) -> None:
        """Print an error message to the screen.

        Args:
            message (str): The message printed to the screen.
        """
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )


class StreamLogger:
    """Implements a logger printing to std out.

    Attrs:
        _logging_level (int): The level at which messages should be displayed.
        _logger (logging.Logger): The logger used to print ot sdt out.
    """

    def __init__(self, logging_level: int):
        """Initialize a logger object that prints to std out.

        Args:
            logging_level (int): The log level.
        """
        self._logging_level = logging_level

        loggmessage_format = logging.Formatter("[%(levelname)s] - %(message)s")

        logger = logging.getLogger(__name__)
        logger.setLevel(logging_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging_level)
        console_handler.setFormatter(loggmessage_format)
        logger.addHandler(console_handler)

        self._logger: logging.Logger = logger

    @property
    def logging_level(self) -> int:
        """The level at which the logger operates."""
        return self._logging_level

    def info(self, message: str) -> None:
        """Print an info message to the screen.

        Args:
            message (str): The message printed to the screen.
        """
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """Print an warning message to the screen.

        Args:
            message (str): The message printed to the screen.
        """
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """Print an error message to the screen.

        Args:
            message (str): The message printed to the screen.
        """
        self._logger.error(message)


@dataclasses.dataclass
class Author:
    """The representation of an author.

    Attrs:
        name (str | none): Fullname of the Author. May contain spaces.
        email (str | none): Email address of the author.
    """

    name: str
    email: str


# === IO Operations
def create_folder(path_to_folder: pathlike, logger: Logger) -> bool:
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


def create_file(path_to_file: pathlike, logger: Logger) -> bool:
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
    logger: Logger
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


# === Usecase specific functions
def create_project_structure(
    project_name: str,
    logger: Logger,
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
        create_folder(folder_name, logger)

    logger.info("Creating files")
    for file_name in toplevel_file_names:
        create_file(file_name, logger)

    logger.info("Creating init-files")
    for init_file in init_files:
        create_file(init_file, logger)

    return True


def get_project_metadata(
    project_name: str,
    description: str | None = None,
    author: Author | None = None
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
    logger: Logger,
    distributable: bool = False,
    author: Author | None = None,
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

    write_contents_to_file(
        pathlib.Path("pyproject.toml"),
        tomli_w.dumps(pyprojcect_contents),
        logger
    )

    if distributable:
        setup_py_contents = (
            "from setuptools import setup"
            "\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    setup()"
        )
        write_contents_to_file(
            pathlib.Path("setup.py"),
            setup_py_contents,
            logger
        )

    return True


def logger_factory(requested_logger: str, logging_level: int = logging.INFO):
    """Create a logger for the script.

    The logger can be used as a debug tool to observe the behaviour of the
    scirpt while its runing.

    Args:
        logging_level: The level which should be logged. Defaults to INFO.

    Returns:
        logger: The logger object which logs to the console.
    """
    loggers = {
        "console": StreamLogger
    }

    return loggers[requested_logger](logging_level)


def setup_cli_arguments() -> argparse.Namespace:
    """Define the CLI Arguments."""
    parser = argparse.ArgumentParser(
        prog="pystrap",
    )

    parser.add_argument(
        "project_name", help="The Name of the project to be bootstrapped."
    )

    parser.add_argument(
        "--author-name", default=None, help="The name of the author"
    )

    parser.add_argument(
        "--author-email", default=None, help="The email address of the author"
    )

    parser.add_argument(
        "--distributable",
        action="store_true",
        help="Create a setup.py file to allow the package to be distributed.",
    )

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Disable logging output"
    )

    return parser.parse_args()


def main() -> None:
    """Run the main method of the programm."""
    logger = logger_factory("console", logging.INFO)
    console_arguments = setup_cli_arguments()
    project = console_arguments.project_name
    author = Author(
        console_arguments.author_name,
        console_arguments.author_email
    )
    distributable = console_arguments.distributable

    create_project_structure(project, logger)
    write_configuration_to_files(
        project, logger, author=author, distributable=distributable
    )

    logger.info("Finished execution")


if __name__ == "__main__":
    main()
