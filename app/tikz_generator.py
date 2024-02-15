
from typing import Dict,List, OrderedDict, Tuple
import random
from app.visualisation import Vertex, Edge, Graph

class TikzCodeGenerator:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def update_nodes(self, data:Dict[str,str]) -> None:
        self._data_nodes={key: value for key, value in data.items() if key != 'orientation' and key != 'chartStyle'}
    
    def generate_tikz_code(self) -> str:
        """
        Generates tikz code
        Returns:
            str: tikz code to be exported
        """
        template = self.template()
        # self.update_nodes(self._parsed_data) #call update again in case data changes
        all_nodes = self.create_tikz_vertices(self.graph)
        # node_links = self.get_next_nodes_and_edges(self._data_nodes)
        # subgraphs = self.create_subgraphs(self._data_nodes)
        code = (
            template["preamble"] + "\n" +
            template["start_tikz"] + self.get_shape_template() + "\n" #+
            # template["start_graph"] + self.get_graph_properties(self._parsed_data) + "\n"
        )
        code += f"% Create nodes \n"
        for main_node_id, representation in all_nodes.items():
            # subgraph = subgraphs.get(main_node_id)
            # if subgraph:
            #     code += f"{representation} // {subgraph}; \n"  
            # else:
            code += f"{representation}; \n"
            
        code += f"% Connect nodes \n"     
       
        # for node_id, connected_nodes in node_links.items():
        #     for node in connected_nodes:
        #         code += f"{node_id}"
        #         edge_label = node[1]
        #         end_node = node[0] if all_nodes.get(node[0]) else "default[as=Default End, terminator]"
        #         edge_id = "E" + str(random.randint(0,1000)) 
        #         if edge_label:
        #             code += f" -- {edge_id}[as={edge_label}] -> [-Latex]{end_node},\n"
        #         else:
        #             code += f" -> [-Latex]{end_node},\n"
       
            
        code += template["end"]    
        
        return code
    
    def create_tikz_vertices(self, graph: Graph) -> OrderedDict[str, str]:
        """Create nodes based on input data"""
        vertices = OrderedDict()
        for vertex in graph.vertices:
            vertex_id = vertex.vertex_id
            label = vertex.label
            node_type = vertex.vertex_type
            # style = self._parsed_data.get("chartStyle",{})
            text_color = vertex.font_color
            # subgraph = detail.get("subgraph")
            fill_color = vertex.shape_fill 
            position = vertex.position
            node_representation = f"\\node[{node_type},draw= black,text={text_color},fill={fill_color}!50]({vertex_id}) at {position} {{{label}}}"
            # shape_color = detail.get("shapeColor",style.get("shapeColor", "black"))
            # if not subgraph:
            #     node_representation = f"\\node[{node_type},draw={shape_color},text={text_color},fill={fill_color}!50]({node_id}) {{{label}}}"
            # else:
            #     node_representation = f"{node_id}[{node_type},draw={shape_color}]"
            vertices[vertex_id] = node_representation
        return vertices
    
    def create_subgraphs(self, data: Dict[str,str]):
        inner_graphs = OrderedDict()
        for node_id, detail in data.items():
            subgraph = detail.get("subgraph")   
            if subgraph:
                data_nodes = {key: value for key, value in subgraph.items() if key != "orientation" and key != "chartStyle"} 
                all_nodes = self.create_nodes(data_nodes)
                temp = ""
                for node_representation in all_nodes.values():
                    temp += f"{node_representation},\n"
                node_links = self.get_next_nodes_and_edges(data_nodes)
                
                connections = ""
                for inner_node_id,attached_nodes in node_links.items():
                    for node in attached_nodes:
                        edge_label = node[1]
                        edge_id = "E"+str(random.randint(1,10000))
                        if edge_label:
                            connections += f"{inner_node_id} -- {edge_id}[as={edge_label}] -> [-Latex]{node[0]}, \n" 
                        else:
                            connections += f"{inner_node_id} -> [-Latex]{node[0]}, \n"
                graph = (f"[layered layout, grow'={self.get_graph_orientation(subgraph)}]"
                         f"{{\n"
                             f"{temp}"
                             f"{connections};"
                             f"}}"
                         )
                inner_graphs[node_id] = graph
        return inner_graphs 

                
            
    # def get_next_nodes_and_edges(self, graph: Graph) -> OrderedDict[str, List[Tuple[str,str]]]:
    #     """get information about next nodes and edges from input data"""
    #     nodes = OrderedDict()
    #     for edge in graph.edges:
    #         next_nodes = detail.get("next",[])
    #         connected_nodes = [(node.get("id",""), node.get("edge",""))  for node in next_nodes]
    #         nodes[node_id] = connected_nodes
        
    #     return nodes
                
    # node [draw,terminator] // [layered layout] {idx1[draw,text=blue,as=a, terminator] -> idx2[as=a]}  
        

    def template(self) -> Dict[str, str]:
        """Generate a template for tikz code"""
        preamble = (r"\usetikzlibrary{graphs,positioning,quotes,shapes.geometric,arrows.meta}"
                    "\n" 
        )
        return {
                "preamble": preamble,
                "start_tikz": r"\begin{tikzpicture}",
                "end": r"\end{tikzpicture}"
                }
       
    def get_shape_template(self)-> str:
        '''Return the shape based on type'''
        # style = self._parsed_data.get("chartStyle",{})
        template = (r"[nodes={}, io/.style={{trapezium,thick,trapezium left angle=70, trapezium right angle=110, minimum width=3cm, minimum height=1cm}}, decision/.style={{diamond, thick,minimum width=3cm, minimum height=1cm}}, terminator/.style={{rectangle, rounded corners=3ex, thick, minimum width=3cm, minimum height=1cm}}, process/.style={{rectangle, thick, minimum width=3cm, minimum height=1cm}}]"
                    # .format(style.get("fontColor","black"))
                    )
        return template
    
    # def get_graph_properties(self, data: Dict[str,str])-> str:
    #     '''Return the graph properties'''
    #     direction = self.get_graph_orientation(data)
    #     edge_color = self._parsed_data.get("chartStyle",{})
    #     properties = r"[layered layout, grow'={}, edges={{{},thick}}]{{".format(direction, edge_color.get("edgeColor", "black"))
    #     return properties
    
    # def get_graph_orientation(self, data: Dict[str,str]) -> str:
    #     orientation = data.get("orientation").lower()
    #     direction = "right" if orientation == "lr" else "down"
    #     return direction
    

# MAJOR 
#TODO: Give a edge a random id, so that it can be reused --DONE
#TODO: fit picture on page and centre
#TODO: handle error when json key is not in specification, maybe have a list of valid keys. extract the keys from the input json as a set and check if they are all in the valid key

# MINOR
# TODO: check edge label id to be able to repeat edge labels
#TODO: edges style: arrow type, a edge can have its own color {a -> [red] b}