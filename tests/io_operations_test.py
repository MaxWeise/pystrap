"""Test operations that write to files and folders.

Created: 09.09.2023
@author: Max Weise
"""

import logging
import os
import pathlib
import subprocess
import unittest

from pystrap import main


class TestFileWriter(unittest.TestCase):
    """Test methods that write to files."""

    def setUp(self):
        """Create the test environment."""
        self._logger = logging.getLogger("TestFileWriterLogger")
        self._test_file = pathlib.Path("test_file.txt")

    def test_create_file(self):
        """Test the correct creation of a file."""
        file_path = self._test_file

        actual = main.create_file(file_path, self._logger)

        file_exists = file_path.exists()
        self.assertTrue(actual)
        self.assertTrue(file_exists)

    def test_create_file_FileExists(self):
        """Test correct behaviour when a file exists."""
        file_path = self._test_file
        with open(file_path, "w+", encoding="utf-8"):
            pass

        actual = main.create_file(file_path, self._logger)
        self.assertTrue(actual)

    def tearDown(self):
        """Cleanup the test environment."""
        if self._test_file.exists():
            os.remove(self._test_file)


class TestDirectoryWriter(unittest.TestCase):
    """Test methods that create directories."""

    def setUp(self):
        """Create the test environment."""
        self._logger = logging.getLogger("TestFileWriterLogger")
        self._test_dir = pathlib.Path("test_dir/")

    def test_create_folder(self):
        """Test the correct creation of a directory."""
        folder_path = self._test_dir

        actual = main.create_folder(folder_path, self._logger)

        folder_exists = folder_path.exists()
        self.assertTrue(actual)
        self.assertTrue(folder_exists)

    def test_create_folder_FolderExists(self):
        """Test correct behaviour when a directory exists."""
        folder_path = self._test_dir
        subprocess.run(["mkdir", folder_path])

        actual = main.create_folder(folder_path, self._logger)
        self.assertTrue(actual)

    def tearDown(self):
        """Cleanup the test environment."""
        if pathlib.Path.exists(self._test_dir):
            os.rmdir(self._test_dir)
