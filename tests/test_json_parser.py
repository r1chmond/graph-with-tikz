from unittest.mock import patch

import pytest

from app.exceptions import FileFormatError, InvalidJSONError
from app.json_parser import parse_json_data

valid_data = """
      {
      "orientation": "rl",
      "idx1": {
        "label": "Start",
        "type": "terminator",
        "next": [
          {
            "id": "idx2",
            "edge": "begin process"
          }
        ],
        "shapeFill": "yellow"
      }
      }
      """
invalid_data = "This is not a valid json"


def test_parse_json_successful() -> None:
    parsed_data = parse_json_data(valid_data)
    expected_data = {
        "orientation": "rl",
        "idx1": {
            "label": "Start",
            "type": "terminator",
            "next": [{"id": "idx2", "edge": "begin process"}],
            "shapeFill": "yellow",
        },
    }
    assert isinstance(parsed_data, dict)
    assert parsed_data == expected_data


def test_parse_invalid_json_catches_json_decode_error() -> None:
    with pytest.raises(InvalidJSONError):
        parse_json_data(invalid_data)


def test_parse_catches_unicode_decode_error() -> None:
    with patch("app.json_parser.json.loads") as mock_loads:
        mock_loads.side_effect = UnicodeDecodeError(
            "utf-8", b"", 0, 0, "Error occurred while decoding json."
        )
        with pytest.raises(FileFormatError):
            parse_json_data("")
