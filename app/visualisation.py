# import networkx as nx
# import matplotlib.pyplot as plt
from collections import OrderedDict
from collections import deque

# class DirectedGraph:
#     def __init__(self):
#         # Create a directed graph
#         G = nx.DiGraph()

#         # Add nodes
#         G.add_node("A",node_color="yellow", node_shape="^",node_size=600)
#         G.add_nodes_from([("B",{"node_color": "red","node_shape":"v", "label": "process"}),("C",{"node_color": "green", "node_shape":"8", "label": "end"})])

#         # Add edges
#         G.add_edge("A", "B")
#         G.add_edge("B", "C")
#         G.add_edge("C", "A")

#         node_color_map=["red", "yellow", "green"]
#         node_shapes=["^","o","D"]

#         # G.nodes[0]["style"] = "blue"
#         # Display the graph
#         # custom_pos = {"A": (0, 0), "B": (1, 1), "C": (2, 0)} # Define the layout for better visualization
#         custom_colors = {"A": "red", "B": "green"}
#         pos = nx.spring_layout(G)
#         # pos = nx.spring_layout(G)
#         nodes_attr = {n: G.nodes[n] for n in G.nodes}
#         print(f"{nodes_attr=}")

#         num_of_nodes = len(G.nodes)
#         nodes = OrderedDict()
#         for n in G.nodes:
#             nodes[n] = G.nodes[n]

#         bbox=dict(facecolor="skyblue", boxstyle="round", pad=0.3)
#         for node in nodes:
#             nx.draw_networkx_nodes(node,pos,node_color=nodes[node]["node_color"])

#         labels = {}
#         for n in nodes:
#             labels[n] = nodes[n]["label"] if "label" in nodes[n] else ""
            
#         # nx.draw_networkx(G,pos,labels=labels,bbox=dict(facecolor="skyblue", boxstyle="round", pad=0.3))
#         nx.draw_networkx_edges(G,pos)
#         nx.draw_networkx_labels(G, pos, labels=labels)


#     def visualise(self): 
#         # Show the plot
#        plt.show()
class Vertex:
    def __init__(self, vertex_id: str,label: str="", layer: int = 0) -> None:
        self.vertex_id = vertex_id
        self.label = label
        self.layer = layer
        self.is_source = False
        self.is_sink = False
    
    def __eq__(self, other: object) -> bool:
        return (self.vertex_id == other.vertex_id and
                self.label == other.label and 
                self.layer == other.layer and 
                self.is_sink == other.is_sink and 
                self.is_source == other.is_source)
    
    def __hash__(self) -> int:
        return hash((self.vertex_id,self.label, self.layer, self.is_source, self.is_sink))
    
    def __repr__(self) -> str:
        symbol = ""
        if self.is_source:
            symbol = "+"
        elif self.is_sink:
            symbol = "-"
        return f"{symbol}{self.label}_{self.layer}"
    
    
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
    def __init__(self, edges: set[Edge]) -> None:
        self.edges = edges
        self.vertices = set()
        self.update_vertices()
       
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
        
    def add_vertex(self,vertex_id: str, label: str, layer: int) -> None:
        vertex = Vertex(vertex_id,label,layer)
        return vertex
    
    def create_edges(self, data: dict[str,str]) -> None:
        data_nodes={key: value for key, value in data.items() if key != 'orientation' and key != 'chartStyle'}
        vertex_mapping = self.create_vertices(data)
        for node_id, detail in data_nodes.items():
            next_nodes = detail.get("next",[])                                                    
            connected_nodes = [(node.get("id",""), node.get("edge",""))  for node in next_nodes]
            head = vertex_mapping[node_id]
            self.edges.update({Edge(head,vertex_mapping[next_id]) for next_id,_ in connected_nodes})
    
    def create_vertices(self, data: dict[str,str]) -> set[Vertex]:
        data_nodes={key: value for key, value in data.items() if key != 'orientation' and key != 'chartStyle'}
        vertex_mapping = {}
        for vertex_id,detail in data_nodes.items():
            label = detail.get("label", "")
            vertex = Vertex(vertex_id,label)
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
    new_graph = Graph(set())
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
        else:
            current_layer += 1
            Z.update(U)
    #func below to be moved to vertex ordering {check if G has proper(all tight edges) layering if not add dummies}
    add_dummy_vertices(graph)
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





