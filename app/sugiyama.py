from app.graph import Graph
from app.graph import Vertex
from app.data import ParsedData
from typing import Dict
from typing import List
import copy
from collections import defaultdict



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
    
def topological_ordering(graph: Graph) -> List[Vertex]:
    ''' Kahn's algorithm O(|V|+|E|)'''
    sorted_vertices = []
    source_vertices = graph.get_source_vertices()
    marked = set()
    while source_vertices:
        vertex = source_vertices.pop()
        sorted_vertices.append(vertex)
        for edge in graph.outgoing_non_back_edges(vertex):
            if edge not in marked:
                marked.add(edge)
                tail = edge.tail
                if all(in_edge in marked for in_edge in graph.incoming_non_back_edges(tail)):
                    source_vertices.append(tail)
    
    return sorted_vertices
            
            

def longest_path_layer_assigment(graph: Graph) -> Graph:
    vertices = topological_ordering(graph)
    for vertex in vertices:
        vertex.layer = 1
        
        for edge in graph.incoming_non_back_edges(vertex):
            head = edge.head
            vertex.layer = max(vertex.layer, head.layer+1)
            
    return graph

#TODO: review because dummies arent generated for crossing_example
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

def init_ordering(graph: Graph, vertex: Vertex = None) -> Dict[int, List[Vertex]]:
    if not vertex:
        source_vertices = graph.get_source_vertices()
        if len(source_vertices) > 1:
            raise ValueError("Graph has multiple source vertices")
        vertex = source_vertices[0]

    ordered_vertices = defaultdict(list)

    def dfs(vertex: Vertex):
        ordered_vertices[vertex.layer].append(vertex)
        graph.remove_duplicates(ordered_vertices[vertex.layer])
        for edge in graph.outgoing_non_back_edges(vertex):
            dfs(edge.tail)

    dfs(vertex)

    graph.update_ordering(ordered_vertices)
    return graph.get_ordering()           
        

def adjacent_position(graph: Graph, 
                      ordering: Dict[int, List[Vertex]], 
                      vertex: Vertex,
                      adjacent_layer: int) -> List[int]:
    '''returns a list of the present positions of the vertices adjacent to vertex(v)
    in a given adjacent layer'''
    vertices = ordering[adjacent_layer]
    positions = []
    for edge in graph.incoming_non_back_edges(vertex):
        if edge.head in vertices:
            positions.append(vertices.index(edge.head)+1)
        
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
            neg_median_vertices = []
            for vertex in ordering[layer]:
                median = median_value(graph, ordering, vertex, layer-1)
                medians.append((vertex,median))
                if median < 0:
                    neg_median_vertices.append((ordering[layer].index(vertex),vertex))
                
            ordering[layer] = [v for v,_ in sorted(medians, key=lambda x: x[1])]
            
            #if median of vertex is negative maintain position 
            for index, vertex in neg_median_vertices:
                ordering[layer].remove(vertex)
                ordering[layer].insert(index, vertex)
    
    

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
    max_layer = graph.get_max_layer()
    for i in range(MAX_ITERATIONS):
        weighted_median_sweep(graph,order,i,max_layer)
        transpose(graph, order)
        
        #if crossings in order is less than crossings in previous best
        if overall_crossing(graph, order) < overall_crossing(graph, best):
            best = copy.copy(order)
            
    graph.update_ordering(best)


def vertex_positioning(graph: Graph) -> Graph:
    #set initial x cordinates
    # top_to_bottom(graph)
    interval = 3 #because width of symbols in tikz is 3cm
    y_axis = 1 
    max_layer = graph.get_max_layer()
    for i in range(1, max_layer+1):
        x_axis = 0
        for vertex in graph.get_ordering().get(i):
            vertex.position = x_axis, y_axis
            x_axis += interval+2
        y_axis += interval
    set_orientation(graph)       
    return graph

        
# def top_to_bottom(graph: Graph):
#     '''Throughout functions, the direction of the graph is from bottom to top
#     reverse the direction of the graph'''
#     layer_mapping = defaultdict()
#     max_layer = graph.get_max_layer()
#     j = max_layer
#     for i in range(1, max_layer+1):
#        layer_mapping[i] =  j
#        j -= 1
    
#     for vertex in graph.vertices:
#         vertex.layer = layer_mapping[vertex.layer]
#     ordering = defaultdict(list)
#     for vertices in graph.get_ordering().values():
#        ordering[vertices[0].layer] = vertices     
#     graph.update_ordering(ordering)



def right_to_left(graph: Graph):
    '''90 degrees counter clockwise rotation of the graph(graph has the bottom to top orientation)'''
    for vertex in graph.vertices:
        x, y = vertex.position
        vertex.position = -y, x

def left_to_right(graph: Graph) -> None:
    '''90 degrees clockwise rotation of the graph(graph has the bottom to top orientation)'''
    for vertex in graph.vertices:
        x, y = vertex.position
        vertex.position = y, -x   

def top_to_bottom(graph: Graph) -> None:
    '''Reflection in the x_axis of the graph(graph has the bottom to top orientation)'''
    for vertex in graph.vertices:
        _, y = vertex.position
        vertex.position = _, -y   
         
def set_orientation(graph: Graph):
    match graph.orientation:
        case "dt":
            return
        case "lr":
            left_to_right(graph)
        case "rl":
            right_to_left(graph)
        case _: 
            top_to_bottom(graph)            

#TODO: Test wrong file and wrong json format