
from typing import Dict,List

class TikzCodeGenerator:
    def __init__(self, data: Dict[str, str]) -> None:
        self._parsed_data = data

        
    def generate_tikz_code(self) -> str:
        # print(f'{self._parsed_data=}')
        template = self.template()
        id_list = self.get_nodes()
        code = template["preamble"]
        code = code + "\n" + template["start_tikz"] + self.get_shape_template()
        code = code + "\n" + template["start_graph"] + self.get_graph_properties() + "\n" 
        
        
        for i in range(len(id_list)):
            current_node = id_list[i]
            label = self._parsed_data[current_node].get("label") if self._parsed_data[id_list[i]].get("label") else "   "
            type = self._parsed_data[current_node].get("type") if self._parsed_data[current_node].get("type") else ""
            next_node = self._parsed_data[current_node].get("next") 
            code = code + label + "[" + type + "]"
            if next_node:
                #TODO: work on adding labels - refer to latex proj!!
                code += "--"
        
        
            
        code += template["end"]    
        
        return code
    
    def get_nodes(self) -> List[str]:
        return list(self._parsed_data)
        
    def template(self) -> Dict[str, str]:
        preamble = r"\usetikzlibrary{graphs,graphdrawing,positioning,quotes,shapes.geometric}" \
                  + "\n" + r"\usegdlibrary{layered}"
        return {
                "preamble": preamble,
                "start_tikz": r"\tikz",
                "start_graph": r"\graph",
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
    
