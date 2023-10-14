"""Tests for functions that get and write config.

Created: 13.09.2023
@author: Max Weise
"""

import os
import pathlib
import unittest

from pystrap.config_writers import create_pyprojecttoml_file  # type: ignore
from pystrap.config_writers import get_project_metadata  # type: ignore
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

    def tearDown(self) -> None:
        """Destroy the test environment."""
        if self._test_file.exists():
            os.remove(self._test_file)

class ConfigWriterTest(unittest.TestCase):
    """Test all config writers."""

    def setUp(self):
        """Create the test environment."""
        self._test_file = pathlib.Path("test_file.toml")
        self._empty_logger = _EmptyLogger()

    @unittest.skip("No longer needed")
    def test_get_project_config(self):
        """Test that the attributes get set correctly."""
        project_name = "test_project"

        actual = get_project_metadata(project_name)

        self.assertIsNotNone(actual)
        actual_project_data = actual.get("project", None)
        self.assertIsNotNone(actual_project_data)

        actual_project_name = actual_project_data.get("name", None)
        self.assertIsNotNone(actual_project_name)
        self.assertEqual(actual_project_name, "test_project")

    @unittest.skip("No longer needed")
    def test_get_project_config_withAuthor(self):
        """Test the correct setting of the author."""
        project_name = "test_project"
        author = Author(
            name="Max Mustermann",
            email="max.mustermann@examplemail.com"
        )

        method_return = get_project_metadata(project_name, author=author)
        actual = method_return.get("project", None)

        self.assertIsNotNone(actual)
        self.assertEqual(
            actual.get("authors", None),
            [{
                "name": "Max Mustermann",
                "email": "max.mustermann@examplemail.com"
            }]
        )

    def tearDown(self):
        """Destroy the test environment."""
        if self._test_file.exists():
            os.remove(self._test_file)


if __name__ == "__main__":
    unittest.main()
