# import networkx as nx
# import matplotlib.pyplot as plt
from collections import OrderedDict
from collections import deque
from typing import Dict,List, Set, Tuple
import copy

class Vertex:
    def __init__(self, vertex_id: str,
                 vertex_type: str, 
                 shape_fill: str, 
                 font_color: str,
                 label: str="", 
                 layer: int = 0,
                 position: Tuple[int,int] = (0,0)) -> None:
        self.vertex_id = vertex_id
        self.label = label
        self.layer = layer
        self.vertex_type = vertex_type
        self.shape_fill = shape_fill
        self.font_color = font_color
        self.is_source = False
        self.is_sink = False
        self.position = position
    
    def __eq__(self, other: object) -> bool:
        return (self.vertex_id == other.vertex_id and
                self.label == other.label and 
                self.layer == other.layer and 
                self.is_sink == other.is_sink and 
                self.is_source == other.is_source)
        
    def __ne__(self, other: object) -> bool:
        return not self == other
    
    def __hash__(self) -> int:
        return hash((self.vertex_id,self.label, self.layer, self.is_source, self.is_sink))
    
    def __repr__(self) -> str:
        symbol = ""
        if self.is_source:
            symbol = "+"
        elif self.is_sink:
            symbol = "-"
        return f"{symbol}{self.label}_{self.layer} pos({self.position})"
    
    
class Edge:
    def __init__(self, head: Vertex, tail: Vertex, weight: int = 1) -> None:
        self.head = head
        self.tail = tail
        self.weight = weight
        self.reversed = False 
        
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Edge):
            return self.head == other.head and \
                    self.tail == other.tail and \
                    self.weight == other.weight and \
                    self.reversed == other.reversed
        return False
          
    def __hash__(self) -> int:
        return hash((self.head, self.tail, self.weight))
        
    def __repr__(self) -> str:
        return f"Edge({self.head} --{self.weight}-> {self.tail}) [is_back_edge = {self.reversed}]"
        
class Graph:
    def __init__(self, data: Dict[str,str]) -> None:
        self._parsed_data = data
        self.vertices: Set[Vertex] = set()
        self.edges = self.create_edges(self.get_vertices_from_data(self._parsed_data))
        self.ordering: Dict[int, List[Vertex]] = {}
        # self.update_vertices()
    
    def get_vertices_from_data(self, data: Dict[str,str]) -> Dict[str,str]:
        data_vertices = {key: value for key, value in data.items() if key != 'orientation' and key != 'chartStyle'}
        return data_vertices
    
    def update_vertices(self) -> None:
        for edge in self.edges:
             self.vertices.add(edge.head)
             self.vertices.add(edge.tail)
    
    def get_num_of_vertices(self) -> int:
        return len(self.vertices)
    
    def add_edge(self,head: Vertex, tail: Vertex, weight: int = 1) -> None:
        new_edge = Edge(head,tail,weight)
        self.edges.add(new_edge)
        self.update_vertices()
        
    def add_vertex(self,vertex_id: str, label: str,layer: int, font_color: str = "white", shape_fill: str = "white") -> None:
        vertex = Vertex(vertex_id,"dummy","black",font_color,label,layer)
        return vertex
    
    def create_edges(self, data_vertices: dict[str,str]) -> set[Edge]:
        # data_nodes={key: value for key, value in data.items() if key != 'orientation' and key != 'chartStyle'}
        vertex_mapping = self.create_vertices(data_vertices)
        edges = set()
        for vertex_id, detail in data_vertices.items():
            next_vertices = detail.get("next",[])                                                    
            connected_nodes = [(node.get("id",""), node.get("edge",""))  for node in next_vertices]
            head = vertex_mapping[vertex_id]
            edges.update({Edge(head,vertex_mapping[next_id]) for next_id,_ in connected_nodes})

        return edges
    
    def create_vertices(self, data_vertices: dict[str,str]) -> set[Vertex]:
        # data_nodes={key: value for key, value in data.items() if key != 'orientation' and key != 'chartStyle'}
        vertex_mapping = {}
        for vertex_id,detail in data_vertices.items():
            label = detail.get("label", "")
            vertex_type = detail.get("type", "process")
            style = self._parsed_data.get("chartStyle",{})
            text_color = detail.get("fontColor",style.get("fontColor", "black"))
            # subgraph = detail.get("subgraph")
            fill_color = detail.get("shapeFill",style.get("shapeFill", "white")) 
            # shape_color = detail.get("shapeColor",style.get("shapeColor", "black"))
            vertex = Vertex(vertex_id, vertex_type, fill_color, text_color, label)
            vertex_mapping[vertex_id] = vertex
            self.vertices.add(vertex)
        return vertex_mapping
    
    def all_outgoing_edges(self, vertex: Vertex) -> set[Edge]:
        edges = set()
        for edge in self.edges:
            if edge.head == vertex:
                edges.add(edge)
        
        return edges
    
    def outgoing_non_back_edges(self, vertex: Vertex) -> set[Edge]:
        edges = {edge for edge in self.edges if not edge.reversed and edge.head == vertex} 
        return edges
    

    def all_incoming_edges(self, vertex: Vertex) -> set[Edge]:
        edges = set()
        for edge in self.edges:
            if edge.tail == vertex:
                edges.add(edge)
            
        return edges
    
    def incoming_non_back_edges(self, vertex: Vertex) -> set[Edge]:
        edges = {edge for edge in self.edges if not edge.reversed and edge.tail == vertex} 
        return edges

    def get_vertex(self, vertex_id: str) -> Vertex:
        for v in self.vertices:
            if vertex_id == v.vertex_id:
                return v
        return None
    
    def get_max_layer(self,) -> int:
        '''Return source vertex with the higher layer'''
        max_layer = 0
        for vertex in self.vertices:
            max_layer = max(max_layer, vertex.layer)  
        return max_layer
    
    def get_ordering(self) -> Dict[int, List[Vertex]]:
        return self.ordering
    
    def update_ordering(self, new_ordering: Dict[int, List[Vertex]]) -> None:
        self.ordering = new_ordering
    
    def print_graph(self):
        for edge in self.edges:
            print(edge)
    
