import unittest
import os
from app.file_handler import FileHandler
from app.json_parser import JSONParser
from app.tikz_generator import TikzCodeGenerator
from app.data import ParsedData
from app.graph import Vertex, Edge, Graph
from app import sugiyama

class TestFileHandler(unittest.TestCase):
    
    def setUp(self) -> None:
        self.write_valid_json_file()
        self.handler = FileHandler()
        self.parsed_data = ParsedData(os.path.join("valid.json"))
        self.graph = Graph(self.parsed_data.get_parsed_data())
        self.generator = TikzCodeGenerator(self.graph)
        
    def tearDown(self) -> None:
        try:
            if os.path.exists("exported.tex"):
                os.remove("exported.tex")
            if os.path.exists("valid.json"):
                os.remove("valid.json")
        except OSError as e:
            print(f"Error during tearDown: {e}")
        
    def test_read_file_successful(self) -> None:
        data = self.handler.read("valid.json")
        self.assertIsNotNone(data)

    def test_read_nonexistent_file(self) -> None:
        data = self.handler.read("nonexistent.json")
        self.assertIsNone(data)
    
    def test_write_file_successful(self) -> None:    
        code = self.generator.generate_tikz_code()
        self.handler.write("exported.tex", code)
        
        with open("exported.tex", "r") as file:
            file_content = file.read()
        self.assertIsNotNone(file_content)
    
    def write_valid_json_file(self) -> None:
        data =""" {
    "orientation": "td",
    "idx1": {
        "label": "start",
        "type": "terminator",
        "next": [
            {
                "id": "idx2",
                "edge": "edge"
            },
            {
                "id": "idx3",
                "edge": "desc"
            }
        ]
    },
    "idx2": {
        "label": "go",
        "type": "process",
        "next": [
            {
                "id": "idx3"
            }
            ] 
            } 
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
            
class TestVertex(unittest.TestCase):
    
    def setUp(self) -> None:
        self.v1 = Vertex("v1", "type1", "fill1", "color1", "label1", 2, (10, 20))
        self.v2 = Vertex("v1", "type1", "fill1", "color1", "label1", 2, (10, 20))
        self.v3 = Vertex("v3", "type3", "fill3", "color3", "label3", 2, (10, 20))
    
    def test_vertex_equality(self):
        self.assertEqual(self.v1, self.v2)
        self.assertNotEqual(self.v1,self.v3)
        self.assertNotEqual(self.v2, self.v3)
        
    def test_hash(self):
        self.assertEqual(hash(self.v1), hash(self.v2))
        self.assertNotEqual(hash(self.v1), hash(self.v3))
        
class TestEdge(unittest.TestCase):
    
    def setUp(self) -> None:
        self.v1 = Vertex("v1", "type1", "fill1", "color1", "label1", 2, (10, 20))
        self.v2 = Vertex("v2", "type2", "fill2", "color2", "label2", 2, (10, 20))
        self.v3 = Vertex("v3", "type3", "fill3", "color3", "label3", 2, (10, 20))
        self.edge1 = Edge(self.v1, self.v3)
        self.edge2 = Edge(self.v1, self.v3)
        self.edge3 = Edge(self.v1, self.v2)
        
    
    def test_edge_equality(self):
        self.assertEqual(self.edge1, self.edge2)
        self.assertNotEqual(self.edge1, self.edge3)
        
    def test_hash(self):
        self.assertEqual(hash(self.edge1), hash(self.edge2))
        self.assertNotEqual(hash(self.edge1), hash(self.edge3))

class TestGraph(unittest.TestCase):
    
    def setUp(self) -> None:
        
        self.graph = Graph()
    
    def test_graph(self):
        pass
       

class TestTikzGenerator(unittest.TestCase):
    pass