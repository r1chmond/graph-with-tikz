import json
from typing import Dict

class JSONParser:
    
    def __init__(self, json_data: str) -> None:
        '''Initialise the JSONParser object with JSON data'''
        self.json_data = json_data
    
    def parse_json_data(self) -> Dict[str, str]:
        '''
        Parse JSON data stored in the object.
        Returns:
        Dict[str, str] -- A dictionary containing the parsed JSON data.
        Raises:
        json.JSONDecodeError -- If there is an error decoding the JSON data.
        '''
        try:
            parsed_json = json.loads(self.json_data)
            return parsed_json
        except json.JSONDecodeError as e:
            print(f"Error!!! Unable to decode. \n{e}")
            return None
        
    