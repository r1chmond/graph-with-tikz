
from typing import Dict,List, OrderedDict, Tuple
import random
from app.graph import Graph

class TikzCodeGenerator:
    def __init__(self, graph: Graph) -> None:
        ''' 
        Initialise TikzCodeGenerator object
        Args:
            graph (Graph) -- graph to generate tikz code from.
        '''
        self.graph:Graph = graph
        
    def create_tikz_vertices(self,) -> OrderedDict[str, str]:
        '''
        Create TikZ vertex representations based on input data.
        Returns:
            OrderedDict[str, str]: Ordered dictionary containing vertex IDs as keys and TikZ node representations as values.
        '''
        vertices_representation = OrderedDict()
        for vertex in self.graph.get_vertices():
            vertex_id = vertex.vertex_id
            label = vertex.label
            node_type = vertex.vertex_type
            # style = self._parsed_data.get("chartStyle",{})
            text_color = vertex.font_color
            # subgraph = detail.get("subgraph")
            fill_color = vertex.shape_fill 
            position = vertex.position
            if vertex.is_dummy:
                node_representation = f"\\node[{node_type},draw= none, text={text_color},fill={fill_color}!50]({vertex_id}) at {position} {{{label}}}"
            else:
                node_representation = f"\\node[{node_type},draw= black, text={text_color},fill={fill_color}!50]({vertex_id}) at {position} {{{label}}}"
            # shape_color = detail.get("shapeColor",style.get("shapeColor", "black"))
            # if not subgraph:
            #     node_representation = f"\\node[{node_type},draw={shape_color},text={text_color},fill={fill_color}!50]({node_id}) {{{label}}}"
            # else:
            #     node_representation = f"{node_id}[{node_type},draw={shape_color}]"
            vertices_representation[vertex_id] = node_representation
        return vertices_representation
    
    def generate_tikz_code(self) -> str:
        """
        Generates tikz code
        Returns:
            str: tikz code to be exported
        """
        template = self.template()
        all_nodes = self.create_tikz_vertices()
        code = (
            template["preamble"] + "\n" +
            template["start_tikz"] + self.get_shape_template() + "\n" 
        )
        # Generate code for nodes first
        code += f"% Create nodes \n"
        for _, representation in all_nodes.items():
            code += f"{representation}; \n"
            
        code += f"% Connect nodes \n" 
            
        # Generate code for connecting nodes
        for edge in self.graph.edges:
            # Handle different cases of edges
            if edge.head.is_dummy and edge.tail.is_dummy:
                code += f"\\draw ({edge.head.vertex_id}.center) -- ({edge.tail.vertex_id}.center); \n"             
            elif edge.head.is_dummy:
                code += f"\\draw[-{{Latex}}] ({edge.head.vertex_id}.center) -- ({edge.tail.vertex_id}); \n"
            elif edge.tail.is_dummy:
                code += f"\\draw ({edge.head.vertex_id}) -- ({edge.tail.vertex_id}.center); \n"
            else:
                code += f"\\draw[-{{Latex}}] ({edge.head.vertex_id}) -- ({edge.tail.vertex_id}); \n"
                    
        code += template["end"]    
        
        return code
    
    
    
    # def create_subgraphs(self, data: Dict[str,str]):
    #     inner_graphs = OrderedDict()
    #     for node_id, detail in data.items():
    #         subgraph = detail.get("subgraph")   
    #         if subgraph:
    #             data_nodes = {key: value for key, value in subgraph.items() if key != "orientation" and key != "chartStyle"} 
    #             all_nodes = self.create_nodes(data_nodes)
    #             temp = ""
    #             for node_representation in all_nodes.values():
    #                 temp += f"{node_representation},\n"
    #             node_links = self.get_next_nodes_and_edges(data_nodes)
                
    #             connections = ""
    #             for inner_node_id,attached_nodes in node_links.items():
    #                 for node in attached_nodes:
    #                     edge_label = node[1]
    #                     edge_id = "E"+str(random.randint(1,10000))
    #                     if edge_label:
    #                         connections += f"{inner_node_id} -- {edge_id}[as={edge_label}] -> [-Latex]{node[0]}, \n" 
    #                     else:
    #                         connections += f"{inner_node_id} -> [-Latex]{node[0]}, \n"
    #             graph = (f"[layered layout, grow'={self.get_graph_orientation(subgraph)}]"
    #                      f"{{\n"
    #                          f"{temp}"
    #                          f"{connections};"
    #                          f"}}"
    #                      )
    #             inner_graphs[node_id] = graph
    #     return inner_graphs 
 
    def template(self) -> Dict[str, str]:
        '''
        Generate a template for TikZ code.
        Returns:
            Dict[str, str]: Dictionary containing TikZ code template components.
        '''
        # Define the preamble containing necessary TikZ libraries
        preamble = (r"\usetikzlibrary{graphs,positioning,quotes,shapes.geometric,arrows.meta}"
                    "\n" 
        )
        return {
                "preamble": preamble,
                "start_tikz": r"\begin{tikzpicture}",
                "end": r"\end{tikzpicture}"
                }
       
    def get_shape_template(self)-> str:
        '''
        get all shape templates
        Returns:
            str -- String representing the shape templates for different vertex types in TikZ.
        '''
        template = (r"[nodes={}, io/.style={{trapezium,thick,trapezium left angle=70, trapezium right angle=110, minimum width=3cm, minimum height=1cm}}, decision/.style={{diamond, thick,minimum width=3cm, minimum height=1cm}}, terminator/.style={{rectangle, rounded corners=3ex, thick, minimum width=3cm, minimum height=1cm}}, process/.style={{rectangle, thick, minimum width=3cm, minimum height=1cm}},dummy/.style={{rectangle, minimum size=1mm, text opacity=0}}]"
                    )
        return template
    
# MAJOR 
#TODO: handle error when json key is not in specification, maybe have a list of valid keys. extract the keys from the input json as a set and check if they are all in the valid key

# MINOR
# TODO: check edge label id to be able to repeat edge labels
#TODO: edges style: arrow type, a edge can have its own color {a -> [red] b}