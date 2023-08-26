"""Main method for the python-bootstrap skript.

Created: 22.08.2023
@author: Max Weise
"""

import argparse
import logging
import pathlib
import subprocess

__version__ = "v1.0.0"
__author__ = "Max Weise"


def create_folder(path_to_folder, logger):
    """Create a folder.

    Args:
        path_to_folder: The path to the folder, relative to the current
            working directory.
    """
    logger.info(f"Creating the folder {path_to_folder}")
    subprocess.run(["mkdir", "-p", path_to_folder])


def create_file(path_to_file, logger):
    """Create a file.

    Args:
        path_to_file: The path to the file, relative to the current
            working directory.
    """
    logger.info(f"Creating the file {path_to_file}")
    subprocess.run(["touch", path_to_file])


def write_contents_to_file(path_to_file, contents, logger):
    """Write a string to an already existing file.

    Args:
        path_to_file: The file which is written to.
        contents: The contents of the file as strings.
    """
    logger.info(f"Writing to {path_to_file}")
    with open(path_to_file, "w", encoding="utf-8") as f:
        f.write(contents)


def create_project_structure(project_name, logger):
    """Create all necessary folders and configuration files.

    Args:
        project_name: The name of the project.
    """
    toplevel_file_names = ["pyproject.toml", "setup.cfg", "setup.py"]
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


def write_configuration_to_files(project_name, logger, description=None):
    """Write configuration data to the configuration files.

    Args:
        project_name: The name of the product.
    """
    logger.info("Writing contents to files")
    pyprojcect_contents = (
        "[build-system]"
        "\nrequires = ["
        '\n    "setuptools>=42",'
        '\n    "wheel"'
        "\n]"
        '\nbuild-backend = "setuptools.build_meta"'
    )
    write_contents_to_file(pathlib.Path("pyproject.toml"), pyprojcect_contents, logger)

    if not description:
        description = "This project has been created with pystrap."

    setup_cfg_contents = (
        "[metadata]"
        f"\nname = {project_name}"
        f"\ndiscription = {description}"
        "\nauthor = Max Weise"
        "\nlicense = MIT"
        "\nlicense_file = LICENSE"
        "\nplatforms = unix, linux, osx, cygwin, win32"
        "\nclassifiers ="
        "\n    Programming Language :: Python :: 3 :: Only"
        "\n    Programming Language :: Python :: 3.10"
        ""
        "\n[options]"
        f"\npackages = {project_name}"
        "\npython_requires = >=3.10"
        "\npackage_dir = src"
        "\nzip_safe = no"
    )
    write_contents_to_file(pathlib.Path("setup.cfg"), setup_cfg_contents, logger)

    setup_py_contents = (
        "from setuptools import setup"
        "\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    setup()"
    )
    write_contents_to_file(pathlib.Path("setup.py"), setup_py_contents, logger)


def logger_factory(logging_level=logging.INFO):
    """Create a logger for the script.

    The logger can be used as a debug tool to observe the behaviour of the
    scirpt while its runing.
    """
    loggmessage_format = logging.Formatter("[%(levelname)s] - %(message)s")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(loggmessage_format)
    logger.addHandler(console_handler)

    return logger


def setup_cli_arguments():
    """Define the CLI Arguments."""
    parser = argparse.ArgumentParser(
        prog="pystrap",
        usage="py main.py project_name",
        epilog=f"This is version {__version__}. The script is created and maintained by {__author__}",
    )

    parser.add_argument(
        "project_name", help="The Name of the project to be bootstrapped."
    )

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Disable logging output"
    )

    return parser.parse_args()


def main() -> None:
    """Run the main method of the programm."""
    logger = logger_factory()
    console_arguments = setup_cli_arguments()
    project = console_arguments.project_name

    create_project_structure(project, logger)
    write_configuration_to_files(project, logger)

    logger.info("Finished execution")


if __name__ == "__main__":
    main()
