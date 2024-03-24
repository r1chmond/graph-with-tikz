from app.json_parser import JSONParser
from app.file_handler import FileHandler
from typing import Dict,List
import os

class ParsedData:
    def __init__(self,path: str) -> None:
        '''Initialise ParsedData object'''
        self._path = os.path.join(path)  
        self._handler = FileHandler()
        self._parsed_data = JSONParser(self._handler.read(self._path)).parse_json_data()
        
    def get_parsed_data(self,) -> Dict[str, str]:
        '''Return a dictionary containing parsed JSON data'''
        return self._parsed_data