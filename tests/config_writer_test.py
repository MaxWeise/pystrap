"""Tests for functions that get and write config.

Created: 13.09.2023
@author: Max Weise
"""

import subprocess
import unittest
import os
import pathlib
from typing import Any

from pystrap import main  # type: ignore


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


class ConfigWriterTest(unittest.TestCase):
    """Test all config writers."""

    def setUp(self):
        """Create the test environment."""
        self._test_file = pathlib.Path("test_file.toml")
        self._empty_logger = _EmptyLogger()

    def test_get_project_config(self):
        """Test that the attributes get set correctly."""
        project_name = "test_project"

        actual = main.get_project_metadata(project_name)

        self.assertIsNotNone(actual)
        actual_project_data = actual.get("project", None)
        self.assertIsNotNone(actual_project_data)

        actual_project_name = actual_project_data.get("name", None)
        self.assertIsNotNone(actual_project_name)
        self.assertEqual(actual_project_name, "test_project")

    def test_get_project_config_withAuthor(self):
        """Test the correct setting of the author."""
        project_name = "test_project"
        author = main.Author(
            name="Max Mustermann",
            email="max.mustermann@examplemail.com"
        )

        method_return = main.get_project_metadata(project_name, author=author)
        actual = method_return.get("project", None)

        self.assertIsNotNone(actual)
        self.assertEqual(
            actual.get("authors", None),
            [{
                "name": "Max Mustermann",
                "email": "max.mustermann@examplemail.com"
            }]
        )

    def test_write_contents_to_file(self):
        """Test that contents get written to a file."""
        file_path = self._test_file
        test_contents = "Test Contents"
        subprocess.run(["touch", file_path])

        rv = main.write_contents_to_file(
            file_path,
            test_contents,
            self._empty_logger
        )

        self.assertTrue(rv)

        with open(file_path, "r", encoding="utf-8") as f:
            actual = f.read()
            self.assertEqual(actual, test_contents)

    def test_write_contents_to_file_fileIsNotEmpty(self):
        """Don't override the contents of an existing file."""
        test_file = self._test_file
        existing_contents = "This is a string"

        with open(test_file, "w+", encoding="utf-8") as f:
            f.write(existing_contents)

        rv = main.write_contents_to_file(
            test_file,
            "Other contents",
            self._empty_logger
        )

        self.assertTrue(rv)

        with open(test_file, "r", encoding="utf-8") as f:
            actual = f.read()
            self.assertEqual(actual, existing_contents)


    def tearDown(self):
        """Destroy the test environment."""
        if self._test_file.exists():
            os.remove(self._test_file)



if __name__ == "__main__":
    unittest.main()
