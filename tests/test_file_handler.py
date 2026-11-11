import os
import tempfile
import unittest
from unittest.mock import patch

from app.file_handler import FileHandler


class TestFileHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_data = self.write_valid_json_file()
        self.handler = FileHandler()
        self.addCleanup(self.test_dir.cleanup)

    def test_read_file_successful(self) -> None:
        file_path = os.path.join(self.test_dir.name, "valid.json")
        data = self.handler.read(file_path)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, str)
        self.assertEqual(data, self.original_data)

    def test_read_nonexistent_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            self.handler.read("nonexistent.json")

    def test_read_permission_denied_file(self) -> None:
        with patch(
            "app.file_handler.open",
            side_effect=PermissionError("Error occurred while reading file."),
        ), self.assertRaises(PermissionError):
            self.handler.read("file.json")

    def test_read_io_error_file(self) -> None:
        with patch(
            "app.file_handler.open",
            side_effect=OSError("Error occurred while reading file."),
        ), self.assertRaises(OSError):
              self.handler.read("file.json")

    def test_write_file_successful(self) -> None:
        content = "Some content"
        file_path = os.path.join(self.test_dir.name, "exported.tex")
        self.handler.write(file_path, content)

        with open(file_path, "r") as file:
            file_content = file.read()
        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(file_content, content)

    def test_write_file_unsuccessful(self) -> None:
        file_path = os.path.join(self.test_dir.name, "file.json")
        with patch(
            "app.file_handler.open",
            side_effect=OSError("Error occurred while writing file"),
        ), self.assertRaises(OSError):
            self.handler.write(file_path, "some code")

    def test_write_file_unsuccessful_during_write(self) -> None:
        file_path = os.path.join(self.test_dir.name, "file.json")
        with patch(
            "app.file_handler.open",
        ) as mock_open:
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.write.side_effect = OSError("Error occurred while writing file")
            with self.assertRaises(OSError):
                self.handler.write(file_path, "some code")

    def write_valid_json_file(self) -> str:
        data = """ {
    "orientation": "td",
    "idx1": {
        "label": "start",
        "type": "terminator",
        "next": [
            {
                "id": "idx2",
                "edge": "edge"
            },
            {
                "id": "idx3",
                "edge": "desc"
            }
        ]
    },
    "idx2": {
        "label": "go",
        "type": "process",
        "next": [
            {
                "id": "idx3"
            }
            ] 
            } 
            }"""
        file_path = os.path.join(self.test_dir.name, "valid.json")
        with open(file_path, "w") as file:
            file.write(data)

        return data
