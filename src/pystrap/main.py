"""Main method for the python-bootstrap skript.

Created: 22.08.2023
@author: Max Weise
"""

import argparse
import dataclasses
import datetime
import logging
import pathlib
import subprocess
from typing import Any, Protocol

import bullet  # type: ignore
import tomli_w

# === Type definition
pathlike = pathlib.Path | str


@dataclasses.dataclass
class Author:
    """The representation of an author.

    Attrs:
        name (str | none): Fullname of the Author. May contain spaces.
        email (str | none): Email address of the author.
    """

    name: str
    email: str


class UI:
    """Provide an interface in the terminal for the user to input data.

    Note: All Attributes default to None.

    Attributes:
        _project_name (str | None): The name of the project.
        _auhtor_name (str | None): The name of the author.
        _auhtor_email (str | None): The Email of the author.
        _distributable (bool): Indicates if the package will
            be uploaded to PyPi.
    """

    def __init__(self) -> None:
        """Initialize an object that handles interactions with the UI."""
        self._project_name: str | None = None
        self._auhtor_name: str | None = None
        self._auhtor_email: str | None = None
        self._distributable: bool = False

    @property
    def project_name(self) -> str:
        """The name of the project."""
        if not self._project_name:
            return "example-project"
        else:
            return self._project_name

    @property
    def author(self) -> Author:
        """The name and email adress of the author."""
        name = self._auhtor_name
        email = self._auhtor_email

        return Author(
            name if name else "John Doe",
            email if email else "john.doe@example.com"
        )

    @property
    def distributable(self) -> bool:
        """If the package will be distributed or not."""
        return self._distributable

    def _validate_email(self, email_to_validate: str) -> bool:
        """Perform simple checks on a string to verify it's format.

        Args:
            email_to_validate (str): The email that should be validated.

        Returns:
            bool: True, if the format of the Email is valid. False otherwise.
        """
        if "@" not in email_to_validate:
            return False

        email_parts: list[str] = email_to_validate.split("@")

        if "." not in email_parts[1]:
            return False

        return True

    def ask_project_name(self) -> None:
        """Prompt the user to input the name of the projct."""
        prompt = bullet.Input(prompt="Please give the name of the project: ")
        self._project_name = prompt.launch()

    def ask_author_name(self) -> None:
        """Prompt the user to input the name of the author."""
        prompt = bullet.Input(prompt="Please give the name of the Author: ")
        self._auhtor_name = prompt.launch()

    def ask_author_email(self) -> None:
        """Prompt the user to input the email adress of the author.

        The method will perform validation on the format of the email adress.
        If the format is not valid, a value of None will be set.
        """
        prompt = bullet.Input(
            prompt="Please give the email adress of the author: "
        )
        user_input = prompt.launch()

        if not user_input:
            return

        if self._validate_email(user_input):
            self._auhtor_email = user_input

    def ask_distributable(self) -> None:
        """Ask the user if the package should be uploaded to PyPi."""
        prompt = bullet.YesNo(
                prompt="Do you intend to upload the project ot PyPI?",
                default="N"
        )

        user_input = prompt.launch()
        self._distributable = user_input

    def __repr__(self) -> str:
        """Print a representation of the state of the TUI Client object.

        This method is intended for developer to observe the state of the
        object.
        """
        return (f"{self._project_name=}\n"
                f"{self._auhtor_name=}\n"
                f"{self._auhtor_email=}\n"
                f"{self._distributable=}\n")


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


class FileLogger:
    """Implements a logger that logs to a file.

    The log file will be created and prefixed with the current date and time
    in iso format.

    Attrs:
        _logging_level (int): The level at which messages should be logged.
        _logger (logging.Logger): The logger used to log to a file.
    """

    def __init__(self, logging_level: int):
        """Initialize a logger object that logs to a file.

        Args:
            logging_level (int): The log level.
        """
        self._logging_level = logging_level

        loggmessage_format = logging.Formatter("[%(levelname)s] - %(message)s")

        logger = logging.getLogger(__name__)
        logger.setLevel(logging_level)

        iso_time: str = datetime.datetime.now().isoformat()
        file_handler = logging.FileHandler(
            f"{iso_time}_logfile.txt",
            encoding="utf-8"
        )
        file_handler.setLevel(logging_level)
        file_handler.setFormatter(loggmessage_format)
        logger.addHandler(file_handler)

        self._logger: logging.Logger = logger

    @property
    def logging_level(self) -> int:
        """The level at which the logger operates."""
        return self._logging_level

    def info(self, message: str) -> None:
        """Emit an info message.

        Args:
            message (str): The message emitted.
        """
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """Emit a warning message.

        Args:
            message (str): The message emitted.
        """
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """Emit an error message.

        Args:
            message (str): The message emitted.
        """
        self._logger.error(message)


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
    # check if file is empty. If not, log and return
    # TODO: This should throw an exception and not return True
    with open(path_to_file, "r", encoding="utf-8") as f:
        file_contents: list[str] = f.readlines()
        if file_contents:
            logger.warning("The file is not emtpy. Do not write to file.")
            return True

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
    # TODO: Add file logger
    loggers = {
        "console": StreamLogger,
        "file": FileLogger
    }

    return loggers[requested_logger](logging_level)


def setup_cli_arguments() -> argparse.Namespace:
    """Define the CLI Arguments."""
    parser = argparse.ArgumentParser(
        prog="pystrap",
    )

    mutex_group = parser.add_mutually_exclusive_group(required=True)

    # === required but mutex arguments
    mutex_group.add_argument(
        "--project_name", help="The Name of the project to be bootstrapped."
    )

    mutex_group.add_argument(
        "-i", "--interactive",
        action="store_true",
        default=False,
        help="Activate interactive mode when creating a new project."
    )

    # === optional arguments
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


def run_console_script(console_arguments, logger: Logger) -> None:
    """Run the main method of the programm."""
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


def run_tui(console_arguments: argparse.Namespace, logger: Logger) -> None:
    """Run the terminal interface.

    Prompt the user to interactively insert the needed data.

    Args:
        console_arguments: The arguments given from the console.
        logger (Logger): Logger object that adheres to the defined
            Logger interface.
    """
    _ = console_arguments
    terminal_client = UI()
    terminal_client.ask_project_name()
    terminal_client.ask_author_name()
    terminal_client.ask_author_email()
    terminal_client.ask_distributable()

    project: str = terminal_client.project_name
    author: Author = terminal_client.author
    distributable: bool = terminal_client.distributable

    create_project_structure(project, logger)
    write_configuration_to_files(
        project, logger, author=author, distributable=distributable
    )


def main():
    """Run the main function of the application."""
    console_arguments = setup_cli_arguments()

    if console_arguments.interactive:
        logger = logger_factory("file", logging.INFO)
        run_tui(console_arguments, logger)
    else:
        # Default is console
        logger = logger_factory("console", logging.INFO)
        run_console_script(console_arguments, logger)


if __name__ == "__main__":
    main()
