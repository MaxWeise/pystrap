"""Tests for functions that get and write config.

Created: 13.09.2023
@author: Max Weise
"""

import unittest
from typing import Any

from pystrap import main  # type: ignore


class ConfigWriterTest(unittest.TestCase):
    """Test all config writers."""

    def setUp(self):
        """Create the test environment."""
        return super().setUp()

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

    def tearDown(self):
        """Destroy the test environment."""
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
