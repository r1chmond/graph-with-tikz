import json

from app.custom_log import log


def parse_json_data(data: str) -> object:
    """
    Raises:
    ValueError -- If there is an error decoding the JSON data.
    """
    try:
        parsed_json = json.loads(data)
        return parsed_json
    except ValueError:  # catches JSONDecodeError & UnicodeDecodeError
        log.exception("Error occurred while decoding data.")
        raise
