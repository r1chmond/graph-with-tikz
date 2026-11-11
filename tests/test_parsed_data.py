from unittest.mock import patch

import pytest

from app.data import ParsedData, ValidationError

POSITIVE_TEST_CASES = [
    ({}, {}),
    ({"idx1": {}, "idx2": {}}, {"idx1": {}, "idx2": {}}),
    (
        {
            "1": {
                "label": "name",
                "type": "io",
                "next": ["idx2", "idx3", "idx3", "idx2"],
            },
        },
        {
            "1": {
                "label": "name",
                "type": "io",
                "next": ["idx2", "idx3"],
            },
        },
    ),
    (
        {
            "1": {
                "label": "name",
                "type": "io",
                "next": ["idx2", 1, 2.1],
            },
        },
        {
            "1": {
                "label": "name",
                "type": "io",
                "next": ["idx2", "1", "2.1"],
            },
        },
    ),
    (
        {
            "orientation": "dt",
            "shapeFill": "red",
            "fontColor": "blue",
            "shapeColor": "white",
            "idx1": {
                "label": "name",
                "type": "io",
                "next": ["idx2", "idx3"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
            "idx3": {
                "label": "name",
                "type": "io",
                "next": ["idx4"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
        },
        {
            "orientation": "dt",
            "shapeFill": "red",
            "fontColor": "blue",
            "shapeColor": "white",
            "idx1": {
                "label": "name",
                "type": "io",
                "next": ["idx2", "idx3"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
            "idx3": {
                "label": "name",
                "type": "io",
                "next": ["idx4"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
        },
    ),
    (
        {
            "orientation": "dt",
            "shapeFill": "red",
            "fontColor": "blue",
            "shapeColor": "white",
            1: {
                "label": "name",
                "type": "io",
                "next": ["idx2", "idx3"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
            2.1: {
                "label": "name",
                "type": "io",
                "next": ["idx4"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
        },
        {
            "orientation": "dt",
            "shapeFill": "red",
            "fontColor": "blue",
            "shapeColor": "white",
            "1": {
                "label": "name",
                "type": "io",
                "next": ["idx2", "idx3"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
            "2.1": {
                "label": "name",
                "type": "io",
                "next": ["idx4"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
        },
    ),
    (
        {
            1.1: {
                "label": "name",
                "type": "io",
                "next": ["idx2", "idx3"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
            2.1: {
                "label": "name",
                "type": "io",
                "next": ["idx4"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
        },
        {
            "1.1": {
                "label": "name",
                "type": "io",
                "next": ["idx2", "idx3"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
            "2.1": {
                "label": "name",
                "type": "io",
                "next": ["idx4"],
                "shapeFill": "red",
                "fontColor": "blue",
                "shapeColor": "white",
            },
        },
    ),
]


@pytest.mark.parametrize("data, expected", POSITIVE_TEST_CASES)
def test_good_data_parsed_successfully(data: object, expected: object) -> None:
    with (
        patch("app.data.FileHandler"),
        patch("app.data.JSONParser.parse_json_data", return_value=data),
        patch("app.data.os.path.join"),
    ):
        pd = ParsedData()
        pd.run_parser()

    validated_data = pd.get_validated_data()
    assert validated_data == expected


NEGATIVE_TEST_CASES = [
    (
        {
            "1": {
                "label": "name",
                "type": "io",
                "next": {"idx2": 1},
            },
        },
        ValidationError,
    ),
    ([{"1": {"label": "name", "type": "io", "next": ["idx2"]}}], ValidationError),
    ({"idx1": {"unknown": "unknown"}, "idx2": {}}, ValidationError),
    ({"unknown": "unknown", "idx1": {}}, ValidationError),
]


@pytest.mark.parametrize("data, expected_exception", NEGATIVE_TEST_CASES)
def test_bad_data_fail(data: object, expected_exception: Exception) -> None:
    with (
        patch("app.data.FileHandler"),
        patch("app.data.JSONParser.parse_json_data", return_value=data),
        patch("app.data.os.path.join"),
    ):
        pd = ParsedData()
        with pytest.raises(expected_exception):
            pd.run_parser()
