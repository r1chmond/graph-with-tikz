import os
from typing import Any, TypedDict

from app.constants import GLOBAL_PROP_KEYWORDS, TOP_LEVEL_KEYWORDS, VERTEX_PROP_KEYWORDS


class ValidationError(Exception):
    pass


class ParsedData:
    pass
    # def __init__(self) -> None:
    #     self._path = os.path.join("/")
    #     self._handler = FileHandler()
    #     self._parser = JSONParser()
    #     self._parsed_data: object | None = None

    # def set_path(self, path: str) -> None:
    #     self._path = os.path.join(path)

    # def run_parser(self) -> object:
    #     data = self._parser.parse_json_data(self._handler.read(self._path))
    #     self._parsed_data = self._validate_data(data)
    #     return self._parsed_data
