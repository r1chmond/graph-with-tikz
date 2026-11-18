from json import JSONDecodeError

import pytest

from app.exceptions import InvalidJSONError, ValidationError
from app.json_parser import parse_json_data

SYNTAX_ERROR_LINE_3 = """{
                          "idx1": {}, 
                              []: []
                      }"""
# sys.getrecursionlimit varies by platform so
# keep depth large and far beyond any interpreter's limit
NESTING_DEPTH = 100_000


def test_valid_json_parsed_successfully() -> None:
    assert parse_json_data('{"a": 1}') == {"a": 1}


@pytest.mark.parametrize(
    "data",
    [
        pytest.param("not a valid json", id="plain_text"),
        pytest.param("", id="empty_string"),
        pytest.param("   \n", id="whitespace_only"),
        pytest.param('{"a": 1},', id="trailing_comma"),
        pytest.param("{'a': 1}", id="single_quote"),
        pytest.param('{"a": 1', id="unclosed_brace"),
    ],
)
def test_malformed_json_raises_invalid_json_error(data: str) -> None:
    with pytest.raises(InvalidJSONError):
        parse_json_data(data)


def test_error_message_reports_line_and_column() -> None:
    with pytest.raises(InvalidJSONError, match=r"line 3, column 31"):
        parse_json_data(SYNTAX_ERROR_LINE_3)


def test_invalid_json_error_is_a_validation_error() -> None:
    assert issubclass(InvalidJSONError, ValidationError)


def test_parse_failure_is_caught_as_validation_error() -> None:
    with pytest.raises(ValidationError):
        parse_json_data("invalid json")


def test_original_decode_error_is_chained() -> None:
    with pytest.raises(InvalidJSONError) as e:
        parse_json_data(SYNTAX_ERROR_LINE_3)
    assert isinstance(e.value.__cause__, JSONDecodeError)


@pytest.mark.parametrize(
    "data, key",
    [
        pytest.param("""{"idx1": {}, "idx1": {}}""", "idx1", id="top_level"),
        pytest.param(
            """{"idx1":{"fontColor": "blue", "fontColor": "red"}}""",
            "fontColor",
            id="nested",
        ),
    ],
)
def test_duplicate_key_raise_invalid_json_error(data: str, key: str) -> None:
    with pytest.raises(InvalidJSONError) as e:
        parse_json_data(data)
    assert key in str(e.value)


def test_same_key_in_different_objects_is_allowed() -> None:
    parsed = parse_json_data('{"a": {"label": "x"}, "b": {"label": "y"}}')
    assert parsed == {"a": {"label": "x"}, "b": {"label": "y"}}


def test_excessive_nesting_raises_invalid_json_error() -> None:
    deeply_nested = "[" * NESTING_DEPTH + "]" * NESTING_DEPTH

    with pytest.raises(InvalidJSONError) as e:
        parse_json_data(deeply_nested)
    assert isinstance(e.value.__cause__, RecursionError)


@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param("[]", [], id="empty_list"),
        pytest.param('""', "", id="empty_string"),
        pytest.param("1", 1, id="number"),
        pytest.param('"x"', "x", id="text"),
    ],
)
def test_non_object_top_level_returned_unchanged(data: str, expected: object) -> None:
    parsed = parse_json_data(data)
    assert parsed == expected
