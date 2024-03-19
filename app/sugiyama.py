from app.graph import Graph, Edge
from app.graph import Vertex
from app.data import ParsedData
from typing import Dict
from typing import List
import copy
from collections import defaultdict, deque



def draw_graph(current_filepath: str) -> Graph:
    parsed_data = ParsedData(current_filepath)
    graph = Graph(parsed_data.get_parsed_data())
    dfs_cycle_removal(graph)
    layer_graph = longest_path_layer_assigment(graph)
    add_dummy_vertices(layer_graph)
    init_ordering(layer_graph)
    cross_reduction(layer_graph)
    return x_coordinate_assignment(layer_graph)
    
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
    for edge in graph.get_all_non_back_edges():
        layer_diff = edge.tail.layer - edge.head.layer
        
        if layer_diff > 1:
            start_vertex = edge.head
            edge.head = graph.add_vertex("*1","dummy",edge.head.layer+1)
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
        
        
def cross_reduction(graph: Graph) -> None:
    layer_cross_minimisation(graph)
    sifting(graph)
    
def layer_cross_minimisation(graph: Graph) -> None:
    '''1st phase of the TALA's method for minimising edge crossings'''
    max_iterations = 10
    ordering = graph.get_ordering()
    for i in range(max_iterations):
        for layer in range(1,graph.get_max_layer()):
            vertices = ordering[layer]
            adj_delta = .00
            vertices_adj_delta = []
            for vertex in vertices:
            
                for edge in graph.outgoing_non_back_edges(vertex):
                    tail = edge.tail
                    adj_delta += ordering[tail.layer].index(tail)
                num_of_tail_vertices = len(graph.outgoing_non_back_edges(vertex))
                if num_of_tail_vertices != 0:
                    adj_delta /= num_of_tail_vertices
                adj_delta = abs(adj_delta - ordering[vertex.layer].index(vertex))
                vertices_adj_delta.append((vertex,adj_delta))   
            #sort by adjacent delta
            ordering[layer] = [v for v,_ in sorted(vertices_adj_delta, key=lambda x: x[1])]
                 
def sifting(graph: Graph) -> None:
    '''2nd Phase of TALA's method of minimising edge crossings'''
     #sifting      
    ordering = graph.get_ordering()
    max_iterations = 10
    for j in range(max_iterations):
        vertices_degree = []    
        for vertex in graph.vertices:
            incoming = len(graph.incoming_non_back_edges(vertex))
            outgoing = len(graph.outgoing_non_back_edges(vertex))
            degree = incoming + outgoing
            vertices_degree.append((vertex, degree))
            
        #sort by highest degree
        vertices_q = [v for v,_ in sorted(vertices_degree, key=lambda x: x[1])]
        vertices_q.reverse()
        for vertex in vertices_q:
            vertices_on_layer = ordering.get(vertex.layer)

            best = []
            for sibling in vertices_on_layer:
                crossing = 0
                #swap vertices
                v_index = vertices_on_layer.index(vertex)
                s_index = vertices_on_layer.index(sibling) 
                vertices_on_layer[v_index], vertices_on_layer[s_index] = sibling, vertex
                
                crossing += count_crossing_above_vertex(vertex, graph)
                crossing += count_crossing_below_vertex(vertex, graph)
                best.append((copy.copy(vertices_on_layer), crossing))
                
                #swap vertices back
                v_index = vertices_on_layer.index(vertex)
                s_index = vertices_on_layer.index(sibling)
                vertices_on_layer[v_index], vertices_on_layer[s_index] = sibling, vertex
            
            new_ordering = min(best,key=lambda x: x[1])[0]
            ordering[vertex.layer] = new_ordering
                                
             
    
def count_crossing_above_vertex(vertex: Vertex, graph: Graph) -> int:
    crossing = 0
    incoming_edges = graph.incoming_non_back_edges(vertex)
    for edge in incoming_edges:
        head = edge.head
        tail = edge.tail
    
        head_index = graph.get_ordering().get(head.layer).index(head)
        tail_index = graph.get_ordering().get(tail.layer).index(tail)

        vertices_on_layer = graph.get_ordering().get(head.layer)
        for v_index,v in enumerate(vertices_on_layer):
           outgoing = graph.outgoing_non_back_edges(v)
           for out_edge in outgoing:
               out_edge_tail_index = graph.get_ordering().get(out_edge.tail.layer).index(out_edge.tail)
               if (v_index > head_index and out_edge_tail_index < tail_index) or \
                    (v_index < head_index and out_edge_tail_index > tail_index) :
                        crossing += 1
    
    return crossing

def count_crossing_below_vertex(vertex: Vertex, graph: Graph) -> int:
    crossing = 0
    outgoing_edges = graph.outgoing_non_back_edges(vertex)
    for edge in outgoing_edges:
        head = edge.head
        tail = edge.tail
    
        head_index = graph.get_ordering().get(head.layer).index(head)
        tail_index = graph.get_ordering().get(tail.layer).index(tail)

        vertices_on_layer = graph.get_ordering().get(tail.layer)
        for v_index,v in enumerate(vertices_on_layer):
           incoming = graph.incoming_non_back_edges(v)
           for in_edge in incoming:
               in_edge_head_index = graph.get_ordering().get(in_edge.head.layer).index(in_edge.head)
               if (v_index > tail_index and in_edge_head_index < head_index) or \
                    (v_index < tail_index and in_edge_head_index > head_index) :
                        crossing += 1
    
    return crossing

def x_coordinate_assignment(graph: Graph) -> Graph:
    #Down-sweep
    vertices_position = {v: 0 for v in graph.vertices} # maybe set to relative pos
    
    for _ in range(2):
        down_sweep_assignment(graph, vertices_position)
        up_sweep_assignment(graph, vertices_position)
        
    for vertex, x in vertices_position.items():
        vertex.position = x, vertex.layer*4
    
    set_orientation(graph)
    return graph
           
def down_sweep_assignment(graph:Graph, vertices_position):

    for layer in range(2, graph.get_max_layer()+1):
        layer_vertices = copy.copy(graph.get_ordering().get(layer))
        vertices_indegree = [(v,len(graph.incoming_non_back_edges(v))) for v in layer_vertices]
        layer_vertices = [v for v,_ in sorted(vertices_indegree,key=lambda x: x[1])]
        for vertex in layer_vertices:
            #get positions of vertices above current layer
            incoming_positions = [vertices_position[e.head] for e in graph.incoming_non_back_edges(vertex)]
            
            position = median_position(incoming_positions)
            vertices_position[vertex] = add_vertex(vertex, position, vertices_position, graph.get_ordering())
            
def up_sweep_assignment(graph: Graph, vertices_position):
    
    for layer in range(graph.get_max_layer()-1, 1, -1):
        layer_vertices = copy.copy(graph.get_ordering().get(layer))
        vertices_outdegree = [(v,len(graph.outgoing_non_back_edges(v))) for v in layer_vertices]
        layer_vertices = [v for v,_ in sorted(vertices_outdegree,key=lambda x: x[1])]
        for vertex in layer_vertices:
            #get positions of vertices above current layer
            outgoing_positions = [vertices_position[e.tail] for e in graph.outgoing_non_back_edges(vertex)]
            
            position = median_position(outgoing_positions)
            vertices_position[vertex] = add_vertex(vertex, position, vertices_position,graph.get_ordering()) 
     
def vertex_centrality(graph: Graph):
    '''Brandes algorithm'''   
    betweenness = {v: 0 for v in graph.vertices}
    V = []
    for vertices in graph.get_ordering().values():
        V.extend(vertices)
    for source in V:
        dependencies = {v: 0 for v in graph.vertices}
        predecessors, bfs_tree, num_of_shortest_paths = bfs_single_source_shortest_path(graph, source)          
        for sink in reversed(bfs_tree):
            if sink != source:
                for v in predecessors[sink]:
                    dependencies[v] += (num_of_shortest_paths[v] / num_of_shortest_paths[sink]) * (1 + dependencies[sink])
        
        for sink in graph.vertices:
            if sink != source:
                betweenness[sink] += dependencies[sink]    
    return betweenness

def bfs_single_source_shortest_path(graph: Graph, source: Vertex):
    distances = {v: float("inf") for v in graph.vertices}
    predecessors = {v: [] for v in graph.vertices}
    num_of_shortest_paths = {v: 0 for v in graph.vertices}
    
    bfs_tree = [] # tracks how vertices are visited
    distances[source] = 0

    num_of_shortest_paths[source] = 1 
    queue = deque([(0,source)])
    
    while queue:
        current_distance, current_vertex = queue.popleft()
        bfs_tree.append(current_vertex)
        
        for edge in graph.outgoing_non_back_edges(current_vertex):
            new_distance = current_distance + edge.weight
            neighbour = edge.tail
            if new_distance <= distances[neighbour]:
                distances[neighbour] =  new_distance
                predecessors[neighbour].extend([current_vertex])
                num_of_shortest_paths[neighbour] += num_of_shortest_paths[current_vertex]
                queue.append((new_distance, neighbour))
    
    return predecessors, bfs_tree, num_of_shortest_paths
            
def find_paths(predecessors: Dict[Vertex, List[Vertex]]):
    '''find paths based on predecessors'''
    def dfs(vertex: Vertex, path):
        if not predecessors[vertex]:
            paths.append(((vertex, sink), [vertex]+path ))
        else:
            for predecessor in predecessors[vertex]:
                dfs(predecessor, [vertex]+path)
    paths = []      
    for sink in predecessors:
        for vertex in predecessors[sink]:
            dfs(vertex, [sink])
    
    return paths
   
        
def add_vertex(vertex: Vertex, 
               position: int, 
               vertices_position: Dict[Vertex, int], 
               ordering: Dict[int, List[Vertex]]) -> None:
    #find nearest positioned neighbour
    vertices_on_layer = ordering.get(vertex.layer)
    leftmost = None
    rightmost = None
    leftmost_list = [v for v in vertices_on_layer if vertices_position.get(v) < vertices_position.get(vertex)]
    if leftmost_list:
        leftmost = max(leftmost_list, key=lambda x: vertices_position.get(x))
    rightmost_list = [v for v in vertices_on_layer if vertices_position.get(v) > vertices_position.get(vertex)] 
    if rightmost_list:
        rightmost = min(rightmost_list, key=lambda x: vertices_position.get(x)) 
    
    vertex_width = 3
    vertex_offset = 2
    
    min_x = vertices_position.get(leftmost, 0) + vertex_width + vertex_offset
    max_x = vertices_position.get(rightmost,len(vertices_position)) - vertex_width # using len of positions might be a problem
    
    return min(max(position, min_x), max_x)
      
        
                        
def median_position(vertices_position: List[Vertex]) -> int:
    if not vertices_position: 
        return 0
    
    n = len(vertices_position)
    
    if n%2 != 0:
        return vertices_position[n//2]
    else:
        mid_r = vertices_position[n//2]
        mid_l = vertices_position[(n//2)-1]
        return (mid_r + mid_l)//2      
                    
            
            
            
            

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