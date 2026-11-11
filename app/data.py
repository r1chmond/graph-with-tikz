import os

from app.constants import GLOBAL_PROP_KEYWORDS, TOP_LEVEL_KEYWORDS, VERTEX_PROP_KEYWORDS
from app.file_handler import FileHandler
from app.json_parser import JSONParser


class InvalidKeywordError(ValueError):
    pass


class ParsedData:
    def __init__(self) -> None:
        self._path = os.path.join("/")
        self._handler = FileHandler()
        self._parser = JSONParser()
        self._parsed_data: object | None = None

    def set_path(self, path: str) -> None:
        self._path = os.path.join(path)

    def run_parser(self) -> object:
        data = self._parser.parse_json_data(self._handler.read(self._path))
        self._parsed_data = self._validate_data(data)
        return self._parsed_data

    def _validate_data(self, data: object) -> object:
        if not isinstance(data, dict):
            raise TypeError(
                f"Expected a dict at the top level but got {type(data).__name__}"
            )

        # ensure top level keys are of the same type
        # and its values are dict
        result = {}
        for key, val in data.items():
            if (
                key not in TOP_LEVEL_KEYWORDS
                and key not in GLOBAL_PROP_KEYWORDS
                and not isinstance(val, dict)
            ):
                raise TypeError(
                    f"Expected a dict but got {type(val).__name__}\n key={key}\n value={val}"
                )

            if isinstance(key, (int, float)):
                result[str(key)] = val
            elif not isinstance(key, str):
                raise TypeError("Top level key is not a string, int or float")
            else:
                result[key] = val

        # check that value keys(properties) are valid
        for key, val in data.items():
            new_val = {}

            if key not in TOP_LEVEL_KEYWORDS and key not in GLOBAL_PROP_KEYWORDS:
                for prop, prop_val in val.items():
                    if not (
                        prop in VERTEX_PROP_KEYWORDS or prop in GLOBAL_PROP_KEYWORDS
                    ):
                        raise InvalidKeywordError(f"Unrecognised property {prop!r}")
                    # check 'next' prop's value is a list
                    if prop == "next" and isinstance(prop_val, list):
                        new_next_list = []
                        # remove duplicates and ensure element are of the
                        # same type
                        seen: set[str] = set()
                        for idx in prop_val:
                            if idx not in seen:
                                if isinstance(idx, (int, float)):
                                    new_next_list.append(str(idx))
                                elif isinstance(idx, str):
                                    new_next_list.append(idx)
                                else:
                                    raise TypeError(
                                        f"Expect a list but got {type(idx).__name__}"
                                    )
                            seen.add(idx)

                        new_val["next"] = new_next_list

                    elif prop != "next":
                        new_val[prop] = prop_val
                    else:
                        raise TypeError(
                            f"Expect a list but got {type(prop_val).__name__}"
                        )

                result[str(key)] = new_val

        return result

    def get_validated_data(self) -> object | None:
        return self._parsed_data
