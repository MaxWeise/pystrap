"""Main method for the python-bootstrap skript.

Created: 22.08.2023
@author: Max Weise
"""

import argparse
import logging

import pystrap.config_writers
import pystrap.system_core


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


def run_console_script(
    console_arguments,
    logger: pystrap.system_core.Logger
) -> None:
    """Run the main method of the programm."""
    project = console_arguments.project_name
    author = pystrap.system_core.Author(
        console_arguments.author_name,
        console_arguments.author_email
    )
    distributable = console_arguments.distributable

    pystrap.config_writers.create_project_structure(
        project, logger, distributable
    )

    pystrap.config_writers.create_pyprojecttoml_file(project, author, logger)

    if distributable:
        pystrap.config_writers.create_setuppy_file(logger)

    logger.info("Finished execution")


def run_tui(
    console_arguments: argparse.Namespace,
    logger: pystrap.system_core.Logger
) -> None:
    """Run the terminal interface.

    Prompt the user to interactively insert the needed data.

    Args:
        console_arguments: The arguments given from the console.
        logger (Logger): Logger object that adheres to the defined
            Logger interface.
    """
    _ = console_arguments
    terminal_client = pystrap.system_core.UI()
    terminal_client.ask_project_name()
    terminal_client.ask_author_name()
    terminal_client.ask_author_email()
    terminal_client.ask_distributable()

    project: str = terminal_client.project_name
    author: pystrap.system_core.Author = terminal_client.author
    distributable: bool = terminal_client.distributable

    pystrap.config_writers.create_project_structure(
        project, logger, distributable
    )

    pystrap.config_writers.create_pyprojecttoml_file(project, author, logger)

    if distributable:
        pystrap.config_writers.create_setuppy_file(logger)


def main():
    """Run the main function of the application."""
    console_arguments = setup_cli_arguments()

    if console_arguments.interactive:
        logger = pystrap.system_core.logger_factory("file", logging.INFO)
        run_tui(console_arguments, logger)
    else:
        # Default is console
        logger = pystrap.system_core.logger_factory("file", logging.INFO)
        run_console_script(console_arguments, logger)


if __name__ == "__main__":
    main()
