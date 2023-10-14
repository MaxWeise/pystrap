"""Define the core components of the system.

Created: 04.10.2023
@author: Max Weise
"""

import dataclasses
import datetime
import logging
from typing import Protocol

import bullet  # type: ignore


@dataclasses.dataclass
class Author:
    """The representation of an author.

    Attrs:
        name (str | none): Fullname of the Author. May contain spaces.
        email (str | none): Email address of the author.
    """

    name: str
    email: str

    def to_list(self):
        """Return the name and email adress as a list."""
        return [self.name, self.email]


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
        "console": StreamLogger,
        "file": FileLogger
    }

    return loggers[requested_logger](logging_level)
