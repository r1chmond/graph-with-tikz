from app.data import ParsedData
from typing import Dict,List

class TikzCodeGenerator:
    def __init__(self, data: str) -> None:
        self._parsed_data = data

        
    def generate_tikz_code(self) -> str:
        # print(f'{self._parsed_data=}')
        template = self.template()
        id_list = self.get_nodes()
        code = template["preamble"]
        code = code + "\n" + template["start_tikz"] + self.get_shape_template()
        code = code + "\n" + template["start_graph"] + self.get_graph_properties() + "\n" 
        
        j = 0 # yet to work on positioning
        for i in range(len(id_list)):
            # code = code + "\n" + template["node"].format(0,j,self._parsed_data[id]["type"],id,self._parsed_data[id]["label"])
            # j -= 2
            code = code + id_list[i]
            if i != len(id_list) - 1:
                code += "--"
        
        # for id in id_list:
        #     next_node = self._parsed_data[id].get("next")
        #     if next_node:
        #         code = code + "\n" + template["draw"].format(id,\
        #                                     f'{next_node["edge"]}' if next_node.get("edge") else "",next_node["id"])
            
        code += template["end"]    
        
        return code
    
    def get_nodes(self) -> List[str]:
        return list(self._parsed_data)
        
    def template(self) -> Dict[(str,str)]:
        preamble = r"\usepackage{tikz}" +"\n" +r"\usetikzlibrary{positioning,quotes,shapes.geometric}" \
                  + "\n" + r"\usegdlibrary {layered}"
        return {
                "preamble": preamble,
                "start_tikz": r"\tikz",
                "start_graph": r"\graph",
                # "node": r"\node at ({},{}) [{}] ({}) {{{}}};",
                "end": "\n"+"};"
                }
       
    def get_shape_template(self)-> str:
        '''Return the shape based on type'''
        template = r"[decision/.style={diamond, draw, thick},terminator/.style={rectangle,draw, rounded corners=1.5ex},process/.style={rectangle, draw}]"
        return template
    
    def get_graph_properties(self)-> str:
        '''Return the graph properties'''
        properties = r"[layered layout]{"
        return properties