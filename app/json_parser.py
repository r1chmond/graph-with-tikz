import json

from app.exceptions import InvalidJSONError


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise InvalidJSONError(f"duplicate key {key!r}")
        result[key] = value
    return result


def parse_json_data(data: str) -> object:
    """
    Parse a JSON string

    Raises:
      InvalidJSONError -- If text is not a valid json or has duplicate keys.
    """
    try:
        parsed_json = json.loads(data, object_pairs_hook=_reject_duplicate_keys)
        parsed_json = json.loads(data)
        return parsed_json
    except json.JSONDecodeError as e:
        raise InvalidJSONError(f"line {e.lineno}, column {e.colno}: \n{e.msg}") from e
    except RecursionError as e:
        raise InvalidJSONError("nesting is too deep") from e
