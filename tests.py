import unittest
import os
from file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    
    def setUp(self) -> None:
        self.write_valid_json_file()
        self.handler = FileHandler()
        
    def tearDown(self) -> None:
        os.remove("valid.json")
        
    def test_read_file_successful(self):
        data = self.handler.read("valid.json")
        self.assertIsNotNone(data)

    def test_read_nonexistent_file(self):
        data = self.handler.read("nonexistent.json")
        self.assertIsNone(data)
    
    def write_valid_json_file(self):
        data =""" {
                        "start": {"id": "idx1","type": "terminator", "next": {"id": "idx2"}}, 
                        "walk": {"id":"idx2", "type": "process"}
                    }"""
        with open("valid.json", "w") as file:
            file.write(data)
            
    
      
      
class TestJSONParser(unittest.TestCase):
    pass
    # def write_invalid_json_file(self):
    #     data ="This is not a valid json"
    #     with open("invalid.json", "w") as file:
    #         file.write(data)     
            
if __name__ == '__main__':
    unittest.main()