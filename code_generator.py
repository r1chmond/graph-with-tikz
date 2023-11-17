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
        id_list = self.get_nodes()
        code = template["start"]
        j = 0 # yet to work on positioning
        for id in id_list:
            code = code + "\n" + template["node"].format(0,j,id, self.parsed_data[id]["label"])
            j -= 2
        
        for id in id_list:
            next_node = self.parsed_data[id].get("next")
            if next_node:
                code = code + "\n" + template["draw"].format(id,\
                                            f'{next_node["edge"]}' if next_node.get("edge") else "",next_node["id"])
                
        code = code + "\n" + template["end"]
        return code
    
    def get_nodes(self) -> List[str]:
        return list(self.parsed_data)
        
    def template(self) -> Dict[(str,str)]:
        return {
                "start": r"\begin{tikzpicture}",
                "node" : r"\node at ({},{}) [draw] ({}) {{{}}};",
                "draw": r'\draw ({}) edge ["{}", ->] ({});',
                "end" : r"\end{tikzpicture}"
                }
        
    