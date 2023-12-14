from app.data import ParsedData
from typing import Dict,List

class TikzCodeGenerator:
    def __init__(self, data: str) -> None:
        self._parsed_data = data

        
    def generate_tikz_code(self) -> str:
        template = self.template()
        id_list = self.get_nodes()
        code = template["preamble"]
        code = code + "\n" + template["start_document"]
        code = code + "\n" + template["start_tikz"]
        code = code + self.get_shape_template()
        j = 0 # yet to work on positioning
        for id in id_list:
            code = code + "\n" + template["node"].format(0,j,self._parsed_data[id]["type"],id,self._parsed_data[id]["label"])
            j -= 2
        
        for id in id_list:
            next_node = self._parsed_data[id].get("next")
            if next_node:
                code = code + "\n" + template["draw"].format(id,\
                                            f'{next_node["edge"]}' if next_node.get("edge") else "",next_node["id"])
                
        code = code + "\n" + template["end_tikz"]
        code = code + "\n" + template["end_document"]
        return code
    
    def get_nodes(self) -> List[str]:
        return list(self._parsed_data)
        
    def template(self) -> Dict[(str,str)]:
        preamble = r"\documentclass{article} " + "\n"+ r"\usepackage{tikz}" +"\n" +r"\usetikzlibrary{positioning,quotes,shapes.geometric}"
        return {
                "preamble": preamble,
                "start_document": r"\begin{document}",
                "start_tikz": r"\begin{tikzpicture}",
                "node": r"\node at ({},{}) [{}] ({}) {{{}}};",
                "draw": r'\draw ({}) edge ["{}", ->] ({});',
                "end_tikz": r"\end{tikzpicture}",
                "end_document": r"\end{document}"
                }
       
    def get_shape_template(self)-> str:
        '''Return the shape based on type'''
        template = r"[decision/.style={diamond, draw, thick},terminator/.style={rectangle,draw, rounded corners=1.5ex},process/.style={rectangle, draw}]"
        return template