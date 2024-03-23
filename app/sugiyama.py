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
    add_dummy_vertices(layer_graph)
    init_ordering(layer_graph)
    cross_reduction(layer_graph)
    x_assigned_graph = x_coordinate_assignment(layer_graph)
    undo_reversed_edges(x_assigned_graph)
    return x_assigned_graph
    
def dfs_visit(graph: Graph, vertex: Vertex, visited: set[Vertex], stacked: set[Vertex]) -> None:
    if vertex not in visited:
        visited.add(vertex)
        stacked.add(vertex)

        for edge in graph.all_outgoing_edges(vertex):
            if edge.tail in stacked:      
                edge.reversed = True
                edge.head, edge.tail = edge.tail, edge.head
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
        for edge in graph.all_outgoing_edges(vertex):
            if edge not in marked:
                marked.add(edge)
                tail = edge.tail
                if all(in_edge in marked for in_edge in graph.all_incoming_edges(tail)):
                    source_vertices.append(tail)
    
    return sorted_vertices
            
            

def longest_path_layer_assigment(graph: Graph) -> Graph:
    vertices = topological_ordering(graph)
    for vertex in vertices:
        vertex.layer = 1
        
        for edge in graph.all_incoming_edges(vertex):
            head = edge.head
            vertex.layer = max(vertex.layer, head.layer+1)
            
    return graph

def add_dummy_vertices(graph: Graph) -> None:
    '''add dummies to achieve proper layering i.e 
    when all edges are tight(a span of 1)'''
    dummies = []
    edges_require_dummies = []
    for edge in graph.edges:
        layer_diff = edge.tail.layer - edge.head.layer
        
        if layer_diff > 1:
            start_vertex = edge.head
            edges_require_dummies.append(copy.copy(edge))
            edge.head = graph.add_dummy_vertex("*1","dummy",edge.head.layer+1)
            edge.head.is_dummy = True
            end_vertex = edge.head
            dummies_on_edge = [end_vertex]
            
            for vertex_id in range(2,layer_diff):
                new_vertex = graph.add_dummy_vertex("*"+str(vertex_id),"dummy",end_vertex.layer+1)
                new_vertex.is_dummy = True
                dummies_on_edge.append(new_vertex)
                end_vertex = new_vertex 
            dummies_on_edge.append(start_vertex)
            dummies.append(dummies_on_edge)
    
    for vertices in dummies:
        for i in range(1,len(vertices)):
            for e in edges_require_dummies:
                if e.head in vertices:
                    graph.add_edge(vertices[i], vertices[i-1], 1, e.reversed)

        graph.vertices.extend(vertices)
        graph.remove_duplicates(graph.vertices)


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
        for edge in graph.all_outgoing_edges(vertex):
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
            
                for edge in graph.all_outgoing_edges(vertex):
                    tail = edge.tail
                    adj_delta += ordering[tail.layer].index(tail)
                num_of_tail_vertices = len(graph.all_outgoing_edges(vertex))
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
    for _ in range(max_iterations):
        vertices_degree = []    
        for vertex in graph.vertices:
            incoming = len(graph.all_incoming_edges(vertex))
            outgoing = len(graph.all_outgoing_edges(vertex))
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
    incoming_edges = graph.all_incoming_edges(vertex)
    for edge in incoming_edges:
        head = edge.head
        tail = edge.tail
    
        head_index = graph.get_ordering().get(head.layer).index(head)
        tail_index = graph.get_ordering().get(tail.layer).index(tail)

        vertices_on_layer = graph.get_ordering().get(head.layer)
        for v_index,v in enumerate(vertices_on_layer):
           outgoing = graph.all_outgoing_edges(v)
           for out_edge in outgoing:
               out_edge_tail_index = graph.get_ordering().get(out_edge.tail.layer).index(out_edge.tail)
               if (v_index > head_index and out_edge_tail_index < tail_index) or \
                    (v_index < head_index and out_edge_tail_index > tail_index) :
                        crossing += 1
    
    return crossing

def count_crossing_below_vertex(vertex: Vertex, graph: Graph) -> int:
    crossing = 0
    outgoing_edges = graph.all_outgoing_edges(vertex)
    for edge in outgoing_edges:
        head = edge.head
        tail = edge.tail
    
        head_index = graph.get_ordering().get(head.layer).index(head)
        tail_index = graph.get_ordering().get(tail.layer).index(tail)

        vertices_on_layer = graph.get_ordering().get(tail.layer)
        for v_index,v in enumerate(vertices_on_layer):
           incoming = graph.all_incoming_edges(v)
           for in_edge in incoming:
               in_edge_head_index = graph.get_ordering().get(in_edge.head.layer).index(in_edge.head)
               if (v_index > tail_index and in_edge_head_index < head_index) or \
                    (v_index < tail_index and in_edge_head_index > head_index) :
                        crossing += 1
    
    return crossing

def x_coordinate_assignment(graph: Graph) -> Graph:
    vertices_position = {v: 0 for v in graph.vertices} # maybe set to relative pos
    
    for _ in range(2):
        down_sweep_assignment(graph, vertices_position)
        up_sweep_assignment(graph, vertices_position)
        
    for vertex, x in vertices_position.items():
        vertex.position = x, vertex.layer*4
    
    set_orientation(graph)
    return graph
           
def down_sweep_assignment(graph:Graph, vertices_position):

    for layer in range(0, graph.get_max_layer()+1):
        layer_vertices = graph.get_ordering().get(layer,[])
        
        for vertex in layer_vertices:
            
            incoming_positions = [vertices_position[e.head] for e in graph.all_incoming_edges(vertex)]
            
            position = median_position(incoming_positions)
            vertices_position[vertex] = add_vertex(vertex, position, vertices_position, graph.get_ordering())
            
def up_sweep_assignment(graph: Graph, vertices_position):
    
    for layer in range(graph.get_max_layer(), 1, -1):
        layer_vertices =graph.get_ordering().get(layer) 
       
        for vertex in layer_vertices:
            outgoing_positions = [vertices_position[e.tail] for e in graph.all_outgoing_edges(vertex)]
            position = median_position(outgoing_positions)
            vertices_position[vertex] = add_vertex(vertex, position, vertices_position,graph.get_ordering()) 
     
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
    
    vertex_width = 4
    vertex_offset = 4
    
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

def remove_dummies(graph: Graph) -> None:
    edge_to_remove = []
    edge_to_connect = None
    for edge in graph.edges:
        if edge.head.is_dummy and edge.tail.is_dummy:
            edge_to_remove.append(edge)
        elif edge.head.is_dummy and not edge.tail.is_dummy:
            if not edge_to_connect:
                edge_to_connect = edge
            elif edge_to_connect.tail.is_dummy:
                edge_to_connect.tail = edge.tail
                edge_to_remove.append(edge)
        elif not edge.head.is_dummy and edge.tail.is_dummy:
            if not edge_to_connect:
                edge_to_connect = edge
            elif edge_to_connect.head.is_dummy:
                edge_to_connect.head = edge.head
                edge_to_remove.append(edge)
    
    for edge in edge_to_remove:
        graph.edges.remove(edge)
            
def undo_reversed_edges(graph: Graph) -> None: 
    for edge in graph.edges:
        if edge.reversed:
            edge.head, edge.tail = edge.tail, edge.head   
           

#TODO: Test wrong file and wrong json format