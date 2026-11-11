import json

from app.exceptions import FileFormatError, InvalidJSONError


def parse_json_data(data: str) -> object:
    """
    Raises:
    ValueError -- If there is an error decoding the JSON data.
    """
    try:
        parsed_json = json.loads(data)
        return parsed_json
    except json.JSONDecodeError as e:
        raise InvalidJSONError(f"line {e.lineno}, column {e.colno}: \n{e.msg}") from e
    except UnicodeDecodeError as e:
        raise FileFormatError() from e
