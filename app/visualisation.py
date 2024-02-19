# import networkx as nx
# import matplotlib.pyplot as plt
from collections import OrderedDict
from collections import deque
from typing import Dict,List, OrderedDict, Tuple

class Vertex:
    def __init__(self, vertex_id: str,
                 vertex_type: str, 
                 shape_fill: str, 
                 font_color: str,
                 label: str="", 
                 layer: int = 0,
                 position: Tuple[int, int] = (0,0)) -> None:
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
        self.vertices = set()
        self.edges = self.create_edges(self.get_vertices_from_data(self._parsed_data))
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
        vertex = Vertex(vertex_id,"process",shape_fill,font_color,label,layer)
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
    
    def outgoing_edges(self, vertex: Vertex) -> set[Edge]:
        edges = set()
        for edge in self.edges:
            if edge.head == vertex:
                edges.add(edge)
        
        return edges
    
    def incoming_edges(self, vertex: Vertex) -> set[Edge]:
        edges = set()
        for edge in self.edges:
            if edge.tail == vertex:
                edges.add(edge)
            
        return edges
    
    def get_vertex(self, vertex_id: str) -> Vertex:
        for v in self.vertices:
            if vertex_id == v.vertex_id:
                return v
        return None
    
    # def is_source(self, vertex):
    #     return len(self.incoming_edges(vertex)) == 0
    
    # def is_sink(self, vertex):
    #     return len(self.outgoing_edges(vertex)) == 0
    
    def print_graph(self):
        for edge in self.edges:
            print(edge)
    

    
def dfs_visit(graph: Graph, vertex: Vertex, visited: set[Vertex], stacked: set[Vertex]) -> FileNotFoundError:
    if vertex not in visited:
        visited.add(vertex)
        stacked.add(vertex)

        for edge in graph.outgoing_edges(vertex):
            if edge.tail in stacked:      
                # graph.edges = {e for e in graph.edges if edge != e}
                edge.reversed = True
            else:
                dfs_visit(graph, edge.tail, visited, stacked)
        
        stacked.remove(vertex)
                
def dfs_cycle_removal(graph: Graph) -> Graph:
    new_graph = Graph({})
    visited = set()
    stacked = set()
    
    for v in graph.vertices:
        dfs_visit(graph,v,visited,stacked)  
    
    for e in graph.edges:
        if not e.reversed:
            new_graph.add_edge(e.head, e.tail, e.weight)
    
    # toggle source and sink vertices        
    for v in new_graph.vertices:
        incoming_edges = new_graph.incoming_edges(v)
        if len(incoming_edges) == 0:
            v.is_source = True
    
    for v in new_graph.vertices:
        outgoing_edges = new_graph.outgoing_edges(v)
        v.is_sink = len(outgoing_edges) == 0
            
    return new_graph  

# def init_rank(graph) -> None:
#     # ranking = []
#     scanned = [] #scanned contains a topological sort of vertices
#     graph_copy = Graph(graph.edges)
#     edges = graph.edges
#     vertices = graph.vertices
#     source_vertices = [v for v in vertices if graph.is_source(v)]
#     while source_vertices:
#         scanned.extend(source_vertices)
#         edges = {e for e in edges if e.head not in source_vertices}
#         vertices = {v for v in vertices if v not in source_vertices}
#         graph.edges = edges
#         graph.vertices = vertices
#         source_vertices = [v for v in vertices if graph.is_source(v)]
    
#     for v in scanned:
#         v.layer = 1
        
#         for e in graph_copy.incoming_edges(v):
#             v.layer = max(v.layer, e.tail.layer+1)
            
#     return graph_copy

def longest_path_layer_assigment(graph: Graph):
    U = set() #track of vertices that have been assigned to a layer
    Z = set() #track of vertices whose outgoing neighbors have already been considered
    layer_mapping = {}
    current_layer = 1
    
    while len(U) != len(graph.vertices):
        selected_vertex = None
        for v in graph.vertices:
            if v not in U and all(edge.tail in Z for edge in graph.outgoing_edges(v)):
                selected_vertex = v
                break
        
        if selected_vertex:
            selected_vertex.layer = current_layer
            U.add(selected_vertex)
            if current_layer in layer_mapping:
                layer_mapping[current_layer].append(selected_vertex)
            else:
                layer_mapping[current_layer] = []
                layer_mapping[current_layer].append(selected_vertex)
        else:
            current_layer += 1
            Z.update(U)
            
    #func below to be moved to vertex ordering {check if G has proper(all tight edges) layering if not add dummies}
    # add_dummy_vertices(graph)
            
    #set positions
    
    #add dummies to layer mapping
    # for v in graph.vertices:
    #     layer_vertices = [vertex for vertices in layer_mapping.values() for vertex in vertices]
    #     if v not in layer_vertices:
    #         layer_mapping[v.layer].append(v)
    # INTERVAL = 2        
    # factor = 0
    # for layer, vertices in layer_mapping.items():
    #     if len(vertices) > 1:
    #         for i,v in enumerate(vertices):
    #             v.position = (i+factor, layer*INTERVAL)
    #             factor += 3
    #     else:
    #         vertices[0].position = (0, layer*INTERVAL)
                
    #     factor = 0
            
    # print(f"layer mapping = {layer_mapping}")
    #func below to be moved to vertex ordering {check if G has proper(all tight edges) layering if not add dummies}
    # add_dummy_vertices(graph)
    return graph

    
def add_dummy_vertices(graph: Graph) -> None:
    '''add dummies to achieve proper layering i.e 
    when all edges are tight(a span of 1)'''
    dummies = []
    for edge in graph.edges:
        layer_diff = edge.head.layer - edge.tail.layer
        
        if layer_diff > 1:
            start_vertex = edge.head
            edge.head = graph.add_vertex("*1","dummy",edge.tail.layer+1)
            end_vertex = edge.head
            dummies_on_edge = [end_vertex]
            
            for vertex_id in range(2,layer_diff):
                new_vertex = graph.add_vertex("*"+str(vertex_id),"dummy",end_vertex.layer+1)
                dummies_on_edge.append(new_vertex)
                end_vertex = new_vertex 
            dummies_on_edge.append(start_vertex)
            dummies.append(dummies_on_edge)
    
    for vertices in dummies:
        for i in range(1,len(vertices)):
                graph.add_edge(vertices[i], vertices[i-1])

        graph.vertices.update(set(vertices))


def promote_vertex(graph: Graph, v: Vertex) -> int:
    dummydiff = 0
    for edge in graph.incoming_edges(v):
        if edge.head.layer == v.layer + 1:
            dummydiff += promote_vertex(graph, edge.head)
            
    v.layer += 1
    dummydiff = dummydiff - len(graph.incoming_edges(v)) + len(graph.outgoing_edges(v))
    return dummydiff

def vertex_promotion_heuristic(graph: Graph) -> None:
    graph_copy = Graph(graph.edges)
    while True:
        promotion = 0
        for v in graph.vertices:
            if len(graph.incoming_edges(v)) > 0:
                if promote_vertex(graph,v) < 0:
                    promotion += 1
                    graph_copy = Graph(graph.edges)
                else:
                    graph = graph_copy
        
        if promotion == 0:
            break
    
    return graph

def init_ordering(graph: Graph):
    # rank_positions = {}
    
    max_layer = -float("inf")
    for vertex in graph.vertices:
        max_layer = max(max_layer, vertex.layer)
    
    rank_positions = {layer: [] for layer in range(1, max_layer+1)}
    
    
    for layer in range(1, max_layer+1):
        queue = deque([vertex for vertex in graph.vertices if vertex.layer == layer])
        position = 0
        
        while queue:
            current_vertex = queue.popleft()
            
            rank_positions[layer].append((current_vertex,position))
            
            position += 1
            
            for edge in graph.incoming_edges(current_vertex):
                for i,v in enumerate(rank_positions[layer]):
                    if edge.head == v[0]:
                        break
                    if i == len(rank_positions[layer])-1:
                        queue.append(edge.head)
    
    return rank_positions                                                                                                                                                                                                                                        

def weighted_median_sweep(graph: Graph, ordering, i: int):
    pass

def median_value(vertex: Vertex, adjacent_rank: int):
    pass

def adjacent_postion(vertex: Vertex, adjacent_rank: int):
    pass

def transpose(ordering):
    pass

def vertex_ordering(graph: Graph):
    pass







