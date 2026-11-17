import os
import tempfile
import unittest
from unittest.mock import patch

from app.exceptions import FileFormatError
from app.file_handler import read, write


class TestFileHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_data = self.write_valid_json_file()
        self.addCleanup(self.test_dir.cleanup)

    def test_read_file_successful(self) -> None:
        file_path = os.path.join(self.test_dir.name, "valid.json")
        data = read(file_path)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, str)
        self.assertEqual(data, self.original_data)

    def test_read_nonexistent_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read("nonexistent.json")

    def test_read_permission_denied_file(self) -> None:
        with (
            patch(
                "app.file_handler.Path.read_text",
                side_effect=PermissionError("Error occurred while reading file."),
            ),
            self.assertRaises(PermissionError),
        ):
            read("file.json")

    def test_read_file_with_invalid_uft8_text(self) -> None:
        with (
            patch(
                "app.file_handler.Path.read_text",
                side_effect=UnicodeDecodeError(
                    "utf-8", b"", 0, 1, "invalid start byte"
                ),
            ),
            self.assertRaises(FileFormatError),
        ):
            read("file.json")

    def test_read_io_error_file(self) -> None:
        with (
            patch(
                "app.file_handler.Path.read_text",
                side_effect=OSError("Error occurred while reading file."),
            ),
            self.assertRaises(OSError),
        ):
            read("file.json")

    def test_write_file_successful(self) -> None:
        content = "Some content"
        file_path = os.path.join(self.test_dir.name, "exported.tex")
        write(file_path, content)

        with open(file_path, "r") as file:
            file_content = file.read()
        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(file_content, content)

    def test_write_file_unsuccessful(self) -> None:
        file_path = os.path.join(self.test_dir.name, "file.json")
        with (
            patch(
                "app.file_handler.os.fdopen",
                side_effect=OSError("Error occurred while writing file"),
            ),
            self.assertRaises(OSError),
        ):
            write(file_path, "some code")

    def test_write_file_unsuccessful_during_write(self) -> None:
        file_path = os.path.join(self.test_dir.name, "file.json")
        with patch(
            "app.file_handler.os.fdopen",
        ) as mock_open:
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.write.side_effect = OSError("Error occurred while writing file")
            with self.assertRaises(OSError):
                write(file_path, "some code")

    def test_write_file_occurs_atomically(self) -> None:
        content = "Some content"
        file_path = os.path.join(self.test_dir.name, "exported.tex")
        with (
            patch("app.file_handler.os.replace", side_effect=OSError()),
            self.assertRaises(OSError),
        ):
            write(file_path, content)

        assert not os.path.exists(file_path)

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
