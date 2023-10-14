"""Tests for functions that get and write config.

Created: 13.09.2023
@author: Max Weise
"""

import os
import pathlib
import unittest
from typing import Any

import tomli
from pystrap.config_writers import create_pyprojecttoml_file  # type: ignore
from pystrap.config_writers import get_project_metadata  # type: ignore
from pystrap.config_writers import create_setuppy_file
from pystrap.system_core import Author  # type: ignore


class _EmptyLogger:
    """This class holds stub methods to adhere to the logger protocoll."""

    def info(self, message: str) -> None:
        """Print an info message to the screen.

        Args:
            message (str): The message printed to the screen.
        """
        # Stub method

    def warning(self, message: str) -> None:
        """Print an warning message to the screen.

        Args:
            message (str): The message printed to the screen.
        """
        # Stub method

    def error(self, message: str) -> None:
        """Print an error message to the screen.

        Args:
            message (str): The message printed to the screen.
        """
        # Stub method


class PyprojecttomlWriterTest(unittest.TestCase):
    """Test methods, that create the pyproject.toml file."""

    def setUp(self) -> None:
        """Create the test environment."""
        self._project_name = "testProject"
        self._auhtor = Author("Test User", "test@user.com")
        self._empty_logger = _EmptyLogger()
        self._test_file = pathlib.Path("testfile_pyproject.toml")

    def _read_file_contents_toml(
        self, file_name: pathlib.Path
    ) -> dict[str, str]:
        with open(file_name, "r", encoding="utf-8") as f:
            file_contents = f.read()
            return tomli.loads(file_contents)

    def _get_expected_file_content_minimal(self) -> dict[str, Any]:
        """Get a minimal verson of the pyproject file contents."""
        project_metadata: dict[str, Any] = {}
        author = self._auhtor

        project_section = {
            "name": self._project_name,
            "version": "0.0.1",
            "authors": author.to_list(),
            "maintainers": author.to_list(),
            "requires-python": ">=3.10"
        }

        buildsystem_section = {
            "requires": [
                "setuptools>=42",
                "wheel"
            ],
            "build-backend": "setuptools.build_meta"
        }

        project_metadata["project"] = project_section
        project_metadata["build-system"] = buildsystem_section

        return project_metadata

    def test_create_pyprojecttoml_file(self):
        """Test the creation of pyproject.toml file."""
        rv = create_pyprojecttoml_file(
            self._project_name,
            self._auhtor,
            self._empty_logger,
            self._test_file
        )

        self.assertTrue(rv)
        self.assertTrue(self._test_file.exists())

        actual_file_contents = self._read_file_contents_toml(self._test_file)
        self.assertNotEqual(
            actual_file_contents.get("project", None),
            None
        )
        self.assertNotEqual(
            actual_file_contents.get("build-system", None),
            None
        )

        expected_file_contents = self._get_expected_file_content_minimal()
        self.assertEqual(actual_file_contents, expected_file_contents)

    def tearDown(self) -> None:
        """Destroy the test environment."""
        if self._test_file.exists():
            os.remove(self._test_file)


class SetuppyWriterTest(unittest.TestCase):
    """Test the correct creation of setup.py."""

    def setUp(self) -> None:
        """Create the test environment."""
        self._empty_logger = _EmptyLogger()
        self._test_file = pathlib.Path("testfile_setup.py")

    def _read_file_contents(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            file_contents = f.read()
            return file_contents

    def test_create_setuppy_file(self):
        """Test the creation of setup.py file."""
        rv = create_setuppy_file(self._empty_logger, self._test_file)

        self.assertTrue(rv)
        actual_file_contents = self._read_file_contents(self._test_file)
        expected_file_contents = (
            "from setuptools import setup"
            "\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    setup()"
        )

        self.assertEqual(actual_file_contents, expected_file_contents)

    def tearDown(self) -> None:
        """Destroy the test environment."""
        if self._test_file.exists():
            os.remove(self._test_file)


if __name__ == "__main__":
    unittest.main()
