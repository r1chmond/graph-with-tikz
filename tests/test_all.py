import unittest
import os
from app.file_handler import FileHandler
from app.json_parser import JSONParser

class TestFileHandler(unittest.TestCase):
    
    def setUp(self) -> None:
        self.write_valid_json_file()
        self.handler = FileHandler()
        
    def tearDown(self) -> None:
        os.remove("valid.json")
        
    def test_read_file_successful(self) -> None:
        data = self.handler.read("valid.json")
        self.assertIsNotNone(data)

    def test_read_nonexistent_file(self) -> None:
        data = self.handler.read("nonexistent.json")
        self.assertIsNone(data)
    
    def write_valid_json_file(self) -> None:
        data =""" {
                        "start": {"id": "idx1","type": "terminator", "next": {"id": "idx2"}}, 
                        "walk": {"id":"idx2", "type": "process"}
                    }"""
        with open("valid.json", "w") as file:
            file.write(data)
            
    
      
      
class TestJSONParser(unittest.TestCase):
    
    def setUp(self) -> None:
        self.handler = FileHandler()
        self.write_invalid_json_file()
        self.write_valid_json_file()
    
    def tearDown(self) -> None:
        os.remove("valid.json")
        os.remove("invalid.json")
    
    def test_parse_json_successful(self) -> None:
        data = self.handler.read("valid.json")
        parser = JSONParser(data)
        parsed_data = parser.parse_json_data()
        self.assertIsNotNone(parsed_data)
    
    def test_parse_invalid_json(self) -> None:
        data = self.handler.read("invalid.json")
        parser = JSONParser(data)
        parsed_data = parser.parse_json_data()
        self.assertIsNone(parsed_data)
        
    def write_valid_json_file(self) -> None:
        data =""" {
                        "start": {"id": "idx1","type": "terminator", "next": {"id": "idx2"}}, 
                        "walk": {"id":"idx2", "type": "process"}
                    }"""
        with open("valid.json", "w") as file:
            file.write(data)
            
    def write_invalid_json_file(self) -> None:
        data ="This is not a valid json"
        with open("invalid.json", "w") as file:
            file.write(data)     
            