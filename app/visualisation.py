import networkx as nx
import matplotlib.pyplot as plt
from collections import OrderedDict

class DirectedGraph:
    def __init__(self):
        # Create a directed graph
        G = nx.DiGraph()

        # Add nodes
        G.add_node("A",node_color="yellow", node_shape="^",node_size=600)
        G.add_nodes_from([("B",{"node_color": "red","node_shape":"v", "label": "process"}),("C",{"node_color": "green", "node_shape":"8", "label": "end"})])

        # Add edges
        G.add_edge("A", "B")
        G.add_edge("B", "C")
        G.add_edge("C", "A")

        node_color_map=["red", "yellow", "green"]
        node_shapes=["^","o","D"]

        # G.nodes[0]["style"] = "blue"
        # Display the graph
        # custom_pos = {"A": (0, 0), "B": (1, 1), "C": (2, 0)} # Define the layout for better visualization
        custom_colors = {"A": "red", "B": "green"}
        pos = nx.spring_layout(G)
        # pos = nx.spring_layout(G)
        nodes_attr = {n: G.nodes[n] for n in G.nodes}
        print(f"{nodes_attr=}")

        num_of_nodes = len(G.nodes)
        nodes = OrderedDict()
        for n in G.nodes:
            nodes[n] = G.nodes[n]

        bbox=dict(facecolor="skyblue", boxstyle="round", pad=0.3)
        for node in nodes:
            nx.draw_networkx_nodes(node,pos,node_color=nodes[node]["node_color"])

        labels = {}
        for n in nodes:
            labels[n] = nodes[n]["label"] if "label" in nodes[n] else ""
            
        # nx.draw_networkx(G,pos,labels=labels,bbox=dict(facecolor="skyblue", boxstyle="round", pad=0.3))
        nx.draw_networkx_edges(G,pos)
        nx.draw_networkx_labels(G, pos, labels=labels)


    def visualise(self): 
        # Show the plot
       plt.show()

class Edge:
    def __init__(self,head,tail,weight):
        self.head = head
        self.tail = tail
        self.weight = weight
        self.reversed = False 
        
    
    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.head == other.head and \
                    self.tail == other.tail and \
                    self.weight == other.weight and \
                    self.reversed == other.reversed
        return False
          
    def __hash__(self):
        return hash((self.head, self.tail, self.weight))
        
    def __repr__(self) -> str:
        return f"Edge({self.head} --{self.weight}-> {self.tail}) [is_back_edge = {self.reversed}]"
        
class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.vertices = set()
        self.update_vertices()
       
    def update_vertices(self):
        for edge in self.edges:
             self.vertices.add(edge.head)
             self.vertices.add(edge.tail)
    
    def get_num_of_vertices(self):
        return len(self.vertices)
    
    def add_edge(self,head,tail,weight):
        new_edge = Edge(head,tail,weight)
        self.edges.add(new_edge)
        self.update_vertices()
    
    def outgoing_edges(self, vertex):
        edges = set()
        for edge in self.edges:
            if edge.head == vertex:
                edges.add(edge)
        
        return edges
    
    def incoming_edges(self, vertex):
        edges = set()
        for edge in self.edges:
            if edge.tail == vertex:
                edges.add(edge)
            
        return edges
    
    def is_source(self, vertex):
        return len(self.incoming_edges(vertex)) == 0
    
    def is_sink(self, vertex):
        return len(self.outgoing_edges(vertex)) == 0
    
    def print_graph(self):
        for edge in self.edges:
            print(edge)
    

    
def dfs_visit(graph, vertex, visited, stacked):
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
                
def dfs_cycle_removal(graph):
    new_graph = Graph(set())
    visited = set()
    stacked = set()
    
    for v in graph.vertices:
        dfs_visit(graph,v,visited,stacked)  
    
    for e in graph.edges:
        if not e.reversed:
            new_graph.add_edge(e.head, e.tail, e.weight)
            
    return new_graph  

def init_rank(graph):
    scanned = []
    edges = graph.edges
    vertices = graph.vertices
    source_vertices = [v for v in vertices if graph.is_source(v)]
    while source_vertices:
        scanned.append(source_vertices)
        edges = {e for e in edges if e.head not in source_vertices}
        vertices = {v for v in vertices if v not in source_vertices}
        graph.edges = edges
        graph.vertices = vertices
        source_vertices = [v for v in vertices if graph.is_source(v)]
    
    return scanned
        


