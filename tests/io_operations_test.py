"""Test operations that write to files and folders.

Created: 09.09.2023
@author: Max Weise
"""

import os
import pathlib
import subprocess
import unittest

from pystrap.io_operations import (create_file, create_folder,  # type: ignore
                                   write_contents_to_file)
from pystrap.system_core import FileNotEmptyException  # type: ignore


class TestFileWriter(unittest.TestCase):
    """Test methods that write to files."""

    def setUp(self):
        """Create the test environment."""
        self._test_file = pathlib.Path("test_file.txt")

    def test_create_file(self):
        """Test the correct creation of a file."""
        file_path = self._test_file

        actual = create_file(file_path)

        file_exists = file_path.exists()
        self.assertTrue(actual)
        self.assertTrue(file_exists)

    def test_create_file_FileExists(self):
        """Test correct behaviour when a file exists."""
        file_path = self._test_file
        subprocess.run(["touch", file_path])

        actual = create_file(file_path)

        self.assertTrue(actual)

    def test_write_contents_to_file(self):
        """Test that contents get written to a file."""
        file_path = self._test_file
        test_contents = "Test Contents"
        subprocess.run(["touch", file_path])

        rv = write_contents_to_file(file_path, test_contents)

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

        with self.assertRaises(FileNotEmptyException):
            rv = write_contents_to_file(test_file, "Other contents")

            self.assertTrue(rv)

            with open(test_file, "r", encoding="utf-8") as f:
                actual = f.read()
                self.assertEqual(actual, existing_contents)

    def tearDown(self):
        """Cleanup the test environment."""
        if self._test_file.exists():
            os.remove(self._test_file)


class TestDirectoryWriter(unittest.TestCase):
    """Test methods that create directories."""

    def setUp(self):
        """Create the test environment."""
        self._test_dir = pathlib.Path("test_dir/")

    def test_create_folder(self):
        """Test the correct creation of a directory."""
        folder_path = self._test_dir

        actual = create_folder(folder_path)

        folder_exists = folder_path.exists()
        self.assertTrue(actual)
        self.assertTrue(folder_exists)

    def test_create_folder_FolderExists(self):
        """Test correct behaviour when a directory exists."""
        folder_path = self._test_dir
        subprocess.run(["mkdir", folder_path])

        actual = create_folder(folder_path)
        self.assertTrue(actual)

    def tearDown(self):
        """Cleanup the test environment."""
        if pathlib.Path.exists(self._test_dir):
            os.rmdir(self._test_dir)
