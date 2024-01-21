
from typing import Dict,List, OrderedDict, Tuple

class TikzCodeGenerator:
    def __init__(self, data: Dict[str, str]) -> None:
        self._parsed_data = data

        
    def generate_tikz_code(self) -> str:
        """
        Generates tikz code
        Returns:
            str: tikz code to be exported
        """
        
        template = self.template()
        all_nodes = self.create_nodes(self._parsed_data)
        node_links = self.get_next_nodes_and_edges(self._parsed_data)
        code = (
            template["preamble"] + "\n" +
            template["start_tikz"] + self.get_shape_template() + "\n" +
            template["start_graph"] + self.get_graph_properties(self._parsed_data) + "\n"
        )
                
       
        for node_id, connected_nodes in node_links.items():
            for node in connected_nodes:
                code += all_nodes[node_id]
                edge_label = node[1]
                end_node = all_nodes.get(node[0], "default[terminator]")
                if edge_label:
                    code += f" -- {edge_label} -> {end_node},\n"
                else:
                    code += f" -> {end_node},\n"
       
            
        code += template["end"]    
        
        return code
    
    def create_nodes(self, data: Dict[str,str]) -> OrderedDict[str, str]:
        """Create nodes based on input data"""
        nodes = OrderedDict()
        for node_id,detail in data.items():
            if node_id == "orientation":
                continue
            label = detail.get("label", "     ")
            node_type = detail.get("type", "")
            node_representation = f"{label}[{node_type}]"
            nodes[node_id] = node_representation
        return nodes

    def get_next_nodes_and_edges(self, data: Dict[str,str]) -> OrderedDict[str, List[Tuple[str,str]]]:
        """get information about next nodes and edges from input data"""
        nodes = OrderedDict()
        for node_id, prop in data.items():
            if node_id == "orientation":
                continue
            next_nodes = prop.get("next",[])
            connected_nodes = [(node.get("id",""), node.get("edge",""))  for node in next_nodes]
            nodes[node_id] = connected_nodes
        
        return nodes
                
            
        

    def template(self) -> Dict[str, str]:
        """Generate a template for tikz code"""
        preamble = (r"\usetikzlibrary{graphs,graphdrawing,positioning,quotes,shapes.geometric}"
                    "\n" + 
                    r"\usegdlibrary{layered}"
        )
        return {
                "preamble": preamble,
                "start_tikz": r"\tikz",
                "start_graph": r"\graph",
                "end": "};"
                }
       
    def get_shape_template(self)-> str:
        '''Return the shape based on type'''
        template = r"[decision/.style={diamond, draw, thick},terminator/.style={rectangle,draw, rounded corners=1.5ex, thick},process/.style={rectangle, draw, thick}]"
        return template
    
    def get_graph_properties(self, data: Dict[str,str])-> str:
        '''Return the graph properties'''
        orientation = data.get("orientation").lower()
        direction = "right" if orientation == "lr" else "down"
        properties = r"[layered layout, grow'={}]{{".format(direction)
        return properties
    
#TODO: g_style first, handle error when json key is not in specification