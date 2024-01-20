
from typing import Dict,List, OrderedDict

class TikzCodeGenerator:
    def __init__(self, data: Dict[str, str]) -> None:
        self._parsed_data = data

        
    def generate_tikz_code(self) -> str:
        
        template = self.template()
        all_nodes = self.create_nodes(self._parsed_data)
        node_links = self.get_next_nodes_and_edges(self._parsed_data)
        print(f'{node_links=}')
        print(f'=============')
        print(f'{all_nodes=}')
        code = template["preamble"]
        code = code + "\n" + template["start_tikz"] + self.get_shape_template()
        code = code + "\n" + template["start_graph"] + self.get_graph_properties() + "\n" 
        
       
        for id, connected_nodes in node_links.items():
            for node in connected_nodes:
                code += all_nodes[id]
                code = code + " -> " + "[\"" + node[1] + "\"]"+ all_nodes[node[0]] + "," + "\n"
                
                                
        
            
        code += template["end"]    
        
        return code
    
    def create_nodes(self, data: Dict[str,str]) -> OrderedDict[str, str]:
        nodes = OrderedDict()
        for id,detail in data.items():
            label = detail.get("label", "     ")
            node_type = detail.get("type", "")
            temp = label + "[" + node_type + "]"
            nodes[id] = temp
        return nodes

    def get_next_nodes_and_edges(self, data: Dict[str,str]) -> OrderedDict[str, List[str]]:
        nodes = OrderedDict()
        for id, prop in data.items():
            next_nodes = prop.get("next")
            if next_nodes:
                connected_nodes = [(node.get("id",""), node.get("edge",""))  for node in next_nodes]
                nodes[id] = connected_nodes
        
        return nodes
                
            
        

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
    
