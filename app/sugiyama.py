from app.graph import Graph
from app.graph import Vertex
from app.data import ParsedData
from typing import Dict
from typing import List
import copy
from collections import deque



def draw_graph(current_filepath: str) -> Graph:
    parsed_data = ParsedData(current_filepath)
    graph = Graph(parsed_data.get_parsed_data())
    dfs_cycle_removal(graph)
    layer_graph = longest_path_layer_assigment(graph)
    vertex_ordering(layer_graph)
    return vertex_positioning(layer_graph)
    
def dfs_visit(graph: Graph, vertex: Vertex, visited: set[Vertex], stacked: set[Vertex]) -> None:
    if vertex not in visited:
        visited.add(vertex)
        stacked.add(vertex)

        for edge in graph.all_outgoing_edges(vertex):
            if edge.tail in stacked:      
                edge.reversed = True
            else:
                dfs_visit(graph, edge.tail, visited, stacked)
        
        stacked.remove(vertex)
                
def dfs_cycle_removal(graph: Graph) -> None:
    visited = set()
    stacked = set()
    
    for v in graph.vertices:
        dfs_visit(graph,v,visited,stacked)  
    

def longest_path_layer_assigment(graph: Graph) -> Graph:
    U = set() #track of vertices that have been assigned to a layer
    Z = set() #track of vertices whose outgoing neighbors have already been considered
    layer_mapping = {}
    current_layer = 1
    
    while len(U) != len(graph.vertices):
        selected_vertex = None
        for v in graph.vertices:
            if v not in U and all(edge.tail in Z for edge in graph.outgoing_non_back_edges(v)):
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

        graph.vertices.extend(vertices)
        graph.remove_duplicates(graph.vertices)


def promote_vertex(graph: Graph, v: Vertex) -> int:
    dummydiff = 0
    for edge in graph.incoming_non_back_edges(v):
        if edge.head.layer == v.layer + 1:
            dummydiff += promote_vertex(graph, edge.head)
            
    v.layer += 1
    dummydiff = dummydiff - len(graph.incoming_non_back_edges(v)) + len(graph.outgoing_non_back_edges(v))
    return dummydiff

def vertex_promotion_heuristic(graph: Graph) -> None:
    graph_copy = copy.deepcopy(graph)
    while True:
        promotion = 0
        for v in graph.vertices:
            if len(graph.incoming_non_back_edges(v)) > 0:
                if promote_vertex(graph,v) < 0:
                    promotion += 1
                    graph_copy = copy.deepcopy(graph)
                else:
                    graph = graph_copy
        
        if promotion == 0:
            break
    
    return graph

def init_ordering(graph: Graph) -> Dict[int, List[Vertex]]:
    '''Initially order vertices in each layer using depth first search'''
    ordered_nodes = {i:[] for i in range(1, graph.get_max_layer() + 1)}
    
    visited = []
    #get vertices with minimum layer
    queue = deque([v for v in graph.vertices if v.layer == 1])
    
    while queue:
        current_vertex = queue.popleft()
        
        if current_vertex not in visited:
            
            ordered_nodes[current_vertex.layer].append(current_vertex)

            visited.append(current_vertex)
            for edge in graph.incoming_non_back_edges(current_vertex):
                neighbour = edge.head
                if neighbour not in visited:
                    queue.append(neighbour)
    
    graph.update_ordering(ordered_nodes)
    return graph.get_ordering()

def adjacent_position(graph: Graph, 
                      ordering: Dict[int, List[Vertex]], 
                      vertex: Vertex,
                      adjacent_layer: int) -> List[int]:
    '''returns a list of the present positions of the vertices adjacent to vertex(v)
    in a given adjacent layer'''
    vertices = ordering[adjacent_layer]
    positions = []
    for edge in graph.outgoing_non_back_edges(vertex):
        if edge.tail in vertices:
            positions.append(vertices.index(edge.tail)+1)
        
    return positions   

def median_value(graph: Graph, 
                 ordering: Dict[int, List[Vertex]], 
                 vertex: Vertex, 
                 adjacent_layer: int) -> float:
    '''Calculate the median value of a vertex based on its adjacent vertices' positions in the given adjacent layer'''
    P = adjacent_position(graph, ordering, vertex, adjacent_layer)
    abs_P = abs(len(P))
    mid = abs_P//2
    
    if abs_P == 0:
        return -1.0
    elif abs_P % 2 == 1:
        return P[mid]
    elif abs_P == 2:
        return (P[0]+P[1]) / 2
    else:
        left = P[mid - 1] - P[0]
        right = P[abs_P - 1] - P[mid]
        return (P[mid-1]*right + P[mid]*left)/(left+right) 
   
def weighted_median_sweep(graph: Graph, 
                          ordering: Dict[int, List[Vertex]], 
                          iter: int, 
                          max_layer: int) -> None:
    '''Perform weighted median calculation and sort vertices in each layer during a forward traversal.'''
    if iter % 2 == 0:
        for layer in range(2,max_layer+1): # avoid keyerror: start at layer 2 because layers starts at 1
            medians = []
            
            for vertex in ordering[layer]:
                median = median_value(graph, ordering, vertex, layer-1)
                medians.append((vertex,median))
            
            ordering[layer] = [v for v,_ in sorted(medians, key=lambda x: x[1])]
    
    

def transpose(graph: Graph, 
              ordering: Dict[int, List[Vertex]]) -> None:
    improved = True
    #keep track of changes in ordering
    layer_vertices = []

    while improved:
        improved = False
        for layer in range(1,len(ordering)+1):
            for i in range(len(ordering[layer])-1):
                v = ordering[layer][i]
                w = ordering[layer][i+1]
                
                if crossing(graph,ordering,v,w) > crossing(graph,ordering,w,v):
                    improved = True
                    ordering[layer][i], ordering[layer][i+1] = ordering[layer][i+1], ordering[layer][i]
                    vertices = ordering[layer]
                    if vertices in layer_vertices:
                        improved = False
                    else:
                        layer_vertices.append(copy.copy(vertices))
                    

def overall_crossing(graph: Graph, 
                     ordering: Dict[int, List[Vertex]]) -> int:
    '''go through each layer in the ordering adding the number of crossings
    Return the total number of crossings in the entire ordering'''
    total = 0
    
    for layer in range(1, len(ordering)+1):
        for i in range(len(ordering[layer])-1):
                v = ordering[layer][i]
                w = ordering[layer][i+1]

                total += crossing(graph, ordering, v, w)
                
    return total

    

def crossing(graph: Graph, 
             ordering: Dict[int, List[Vertex]],
             v: Vertex,
             w: Vertex) -> int:
    crossings = 0
    v_tails = {edge.tail for edge in graph.outgoing_non_back_edges(v)}
    w_tails = {edge.tail for edge in graph.outgoing_non_back_edges(w)}
     
    # if vertex is not sink
    if v.layer != 1 or w.layer != 1:
        #loop through vertices below this layer
        for vertex_x in ordering[v.layer-1]:
            #if the vertex is a tail of an edge where v is the head (ie if vertex_x is in v_tails)
            if vertex_x in v_tails: 
                for vertex_y in ordering[w.layer-1]:
                    if vertex_y in w_tails:
                        if (ordering[v.layer-1].index(vertex_x) > ordering[w.layer-1].index(vertex_y) and
                            ordering[v.layer].index(v) < ordering[w.layer].index(w)):
                            crossings += 1
    return crossings

def vertex_ordering(graph: Graph) -> None:
    add_dummy_vertices(graph)
    order = init_ordering(graph)
    best = copy.copy(order)
    MAX_ITERATIONS = 24
    max_layer = len(order)
    for i in range(MAX_ITERATIONS):
        weighted_median_sweep(graph,order,i,max_layer)
        transpose(graph, order)
        
        #if crossings in order is less than crossings in previous best
        if overall_crossing(graph, order) < overall_crossing(graph, best):
            best = copy.copy(order)
            
    graph.update_ordering(best)


def vertex_positioning(graph: Graph) -> Graph:
    #set initial x cordinates
    interval = 3 #because width of symbols in tikz is 3cm
    y_axis = 1 
    for _,vertices in graph.get_ordering().items():
        x_axis = 0
        for vertex in vertices:
            vertex.position = x_axis, y_axis
            # vertex.position[1] = y_axis
            x_axis += interval+2
            # y_axis += interval
        y_axis += interval
    return graph
 
def remove_duplicates(vertices: List[Vertex]) -> List[Vertex]:
    count = {}
    for vertex in vertices:
        if vertex in count:
            count[vertex] += 1
        else:
            count[vertex] = 1
    
    vertices.clear()
    for vertex in count.keys():
        vertices.append(vertex)