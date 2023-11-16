from json_parser import JSONParser
from file_handler import FileHandler
from typing import Dict,List

class TikzCodeGenerator:
    def __init__(self, path: str) -> None:
        self.path = path
        self.handler = FileHandler()
        self.parsed_data = JSONParser(self.handler.read(self.path)).parse_json_data()
    
    def generate_tikz_code(self) -> str:
        template = self.template()
        nodes = self.get_nodes()
        code = template["start"]
        j = 0 # yet to work on positioning
        for label in nodes:
            code = code + "\n" + template["node"].format(0,j,self.parsed_data[label]["id"], label)
            j -= 2
        
        for label in nodes:
            next_node = self.parsed_data[label].get("next")
            if next_node:
                code = code + "\n" + template["draw"].format(self.parsed_data[label]["id"], next_node["id"])
                
        code = code + "\n" + template["end"]
        return code
    
    def get_nodes(self) -> List[str]:
        return list(self.parsed_data)
        
    def template(self) -> Dict[(str,str)]:
        return {
                "start": r"\begin{tikzpicture}",
                "node" : r"\node at ({},{}) [draw] ({}) {{{}}};",
                "draw": r"\draw ({}) -- ({});",
                "end" : r"\end{tikzpicture}"
                }
        
    