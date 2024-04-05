from app.graph import Graph
from app.graph import Vertex
from app.data import ParsedData
from typing import Dict
from typing import List
import copy
from collections import defaultdict


def draw_graph(current_filepath: str) -> Graph:
    parsed_data = ParsedData(current_filepath)
    # create graph from parsed data
    graph = Graph(parsed_data.get_parsed_data())
    # invoke sugiyama framework methods
    dfs_cycle_removal(graph)
    layer_graph = longest_path_layer_assigment(graph)
    add_dummy_vertices(layer_graph)
    init_ordering(layer_graph)
    cross_reduction(layer_graph)
    x_assigned_graph = coordinate_assignment(layer_graph)
    set_orientation(x_assigned_graph)
    undo_reversed_edges(x_assigned_graph)
    return x_assigned_graph


def dfs_visit(graph: Graph, vertex: Vertex, visited: set[Vertex], stacked: set[Vertex]) -> None:
    """
    Performs a depth-first search (DFS) visit on the given vertex in the graph.

    Args:
     graph (Graph) -- The graph to perform DFS on.
     vertex (Vertex) -- The vertex to start the DFS visit from.
     visited (set[Vertex]) -- A set of vertices already visited during the DFS.
     stacked (set[Vertex]) -- A set of vertices currently in the DFS call stack.

    Note:
     This function modifies the visited and stacked sets in place.
     It modifies the graph by setting the `reversed` attribute of certain edges.
    """
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
    """
    Uses dfs visits to remove cycles in the given graph.

    Args:
     graph (Graph) -- The graph to perform cycle removal on.
    """
    visited = set()
    stacked = set()

    for v in graph.get_vertices():
        dfs_visit(graph, v, visited, stacked)


def topological_ordering(graph: Graph) -> List[Vertex]:
    """
    Performs topological ordering of vertices in a directed acyclic graph (DAG)
    using Kahn's algorithm.

    Args:
     graph (Graph) -- The directed acyclic graph to perform topological ordering on.

    Returns:
     List[Vertex] -- A list of vertices in topological order.

    Note:
     The time complexity of Kahn's algorithm is O(|V| + |E|), where |V| is the number of vertices
      and |E| is the number of edges in the graph.
    """
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
                # Check if all incoming edges of the tail vertex are marked
                if all(in_edge in marked for in_edge in graph.all_incoming_edges(tail)):
                    source_vertices.append(tail)

    return sorted_vertices


def longest_path_layer_assigment(graph: Graph) -> Graph:
    """
    Assigns layers to vertices in a graph based on the longest path algorithm.

    Args:
     graph (Graph) -- The graph for which layers are to be assigned.

    Returns:
     Graph -- The graph with layers assigned to vertices.
    """
    vertices = topological_ordering(graph)
    for vertex in vertices:
        vertex.layer = 1

        for edge in graph.all_incoming_edges(vertex):
            head = edge.head
            vertex.layer = max(vertex.layer, head.layer + 1)

    return graph


def add_dummy_vertices(graph: Graph) -> None:
    """
      Add dummy vertices to achieve proper layering, ensuring that all edges have a span of 1.

    Args:
     graph (Graph) -- The graph to which dummy vertices are to be added.
    """
    dummies = []
    edges_require_dummies = []

    # Iterate through all edges in the graph
    for edge in graph.edges:
        layer_diff = edge.tail.layer - edge.head.layer

        if layer_diff > 1:
            start_vertex = edge.head
            edges_require_dummies.append(copy.copy(edge))
            # Add a dummy vertex between the head and tail vertices
            edge.head = graph.add_dummy_vertex("*1", "dummy", edge.head.layer + 1)
            edge.head.is_dummy = True
            end_vertex = edge.head
            dummies_on_edge = [end_vertex]

            # Add additional dummy vertices to bridge the gap in layers
            for vertex_id in range(2, layer_diff):
                new_vertex = graph.add_dummy_vertex("*" + str(vertex_id), "dummy", end_vertex.layer + 1)
                new_vertex.is_dummy = True
                dummies_on_edge.append(new_vertex)

            dummies_on_edge.append(start_vertex)
            dummies.append(dummies_on_edge)

    # Add edges between dummy vertices to maintain connectivity
    for vertices in dummies:
        for i in range(1, len(vertices)):
            for e in edges_require_dummies:
                if e.head in vertices:
                    graph.add_edge(vertices[i], vertices[i - 1], 1, e.reversed)
                    break

        graph.get_vertices().extend(vertices)  # update the graph's vertices with dummy vertices
        graph.remove_duplicates(graph.get_vertices())


def init_ordering(graph: Graph, vertex: Vertex = None) -> None:
    """
    Initialise vertex ordering within layers using depth-first search (DFS) traversal.

    Args:
     graph (Graph) -- The graph for which vertex ordering is to be initialised.
     vertex (Vertex, optional) -- The starting vertex for DFS traversal. If not provided,
      the first source vertex is used as the starting point.
    """
    if not vertex:
        source_vertices = graph.get_source_vertices()
        # if len(source_vertices) > 1:
        #     raise ValueError("Graph has multiple source vertices")
        vertex = source_vertices[0]

    ordered_vertices = defaultdict(list)

    def dfs(current_vertex: Vertex):
        ordered_vertices[current_vertex.layer].append(current_vertex)
        graph.remove_duplicates(ordered_vertices[current_vertex.layer])
        for edge in graph.all_outgoing_edges(current_vertex):
            dfs(edge.tail)

    dfs(vertex)

    graph.update_ordering(ordered_vertices)
    # return graph.get_ordering()           


def cross_reduction(graph: Graph) -> None:
    layer_cross_minimisation(graph)
    sifting(graph)


def layer_cross_minimisation(graph: Graph) -> None:
    """
       Perform the first phase of TALA's(Terrastruct's AutoLayout Approach) method for minimising edge crossings.
    Args:
     graph (Graph) -- The graph for which edge crossings are to be minimised.
    Note:
     This function iteratively optimises the vertex ordering within layers to minimise edge crossings.
      It calculates the "adjacent delta" for each vertex, which represents the difference between its
      current position and the average position of its adjacent vertices in the ordering.
      Vertices are then sorted based on their adjacent delta values, and the ordering within each layer
      is updated accordingly.
    """
    # max_iterations = 10
    ordering = graph.get_ordering()
    not_matching_order = True
    while not_matching_order:
        # for _ in range(max_iterations):
        copy_ordering = copy.copy(ordering)
        for layer in range(1, graph.get_max_layer()):
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
                vertices_adj_delta.append((vertex, adj_delta))
                # sort by adjacent delta
            ordering[layer] = [v for v, _ in sorted(vertices_adj_delta, key=lambda x: x[1])]

        if ordering == copy_ordering:
            not_matching_order = False


def sifting(graph: Graph) -> None:
    """
    Performs the second phase of TALA's(Terrastruct's AutoLayout Approach) method for minimising edge crossings.

    Args:
     graph (Graph) -- The graph for which edge crossings are to be minimised.

    Note:
     The function iteratively optimises the vertex ordering within layers to minimise edge crossings.
      It calculates the degree of each vertex (number of incoming and outgoing edges),
      sorts vertices based on their degrees, and performs vertex swaps to reduce edge crossings.
      The best vertex ordering after swaps is selected based on the minimum number of edge crossings.
    """
    # sifting
    ordering = graph.get_ordering()
    max_iterations = 10
    vertices_degree = []
    # get the degree of each vertex
    for vertex in graph.get_vertices():
        incoming = len(graph.all_incoming_edges(vertex))
        outgoing = len(graph.all_outgoing_edges(vertex))
        degree = incoming + outgoing
        vertices_degree.append((vertex, degree))

    # sort by highest degree
    vertices_q = [v for v, _ in sorted(vertices_degree, key=lambda x: x[1])]
    vertices_q.reverse()
    for _ in range(max_iterations):

        for vertex in vertices_q:
            vertices_on_layer = ordering.get(vertex.layer)

            best = []
            for sibling in vertices_on_layer:
                crossing = 0
                # swap vertices
                v_index = vertices_on_layer.index(vertex)
                s_index = vertices_on_layer.index(sibling)
                vertices_on_layer[v_index], vertices_on_layer[s_index] = sibling, vertex

                crossing += count_crossing_above_vertex(vertex, graph)
                crossing += count_crossing_below_vertex(vertex, graph)
                best.append((copy.copy(vertices_on_layer), crossing))

                # swap vertices back
                # at this point, s_index is the index of vertex
                # and v_index is the index of sibling
                vertices_on_layer[v_index], vertices_on_layer[s_index] = vertex, sibling

            new_ordering = min(best, key=lambda x: x[1])[0]
            ordering[vertex.layer] = new_ordering


def count_crossing_above_vertex(vertex: Vertex, graph: Graph) -> int:
    """
    Counts the number of edges crossing above a given vertex in a graph.

    Args:
     vertex -- The vertex above which crossings are counted.
     graph -- The graph in which crossings are counted.

    Returns:
     (int) -- The number of crossings above the vertex.
    """
    crossing = 0
    incoming_edges = graph.all_incoming_edges(vertex)
    for edge in incoming_edges:
        head = edge.head
        tail = edge.tail

        head_index = graph.get_ordering().get(head.layer).index(head)
        tail_index = graph.get_ordering().get(tail.layer).index(tail)

        vertices_on_layer = graph.get_ordering().get(head.layer)
        for v_index, v in enumerate(vertices_on_layer):
            outgoing = graph.all_outgoing_edges(v)
            for out_edge in outgoing:
                out_edge_tail_index = graph.get_ordering().get(out_edge.tail.layer).index(out_edge.tail)
                if (v_index > head_index and out_edge_tail_index < tail_index) or \
                        (v_index < head_index and out_edge_tail_index > tail_index):
                    crossing += 1

    return crossing


def count_crossing_below_vertex(vertex: Vertex, graph: Graph) -> int:
    """
    Counts the number of edges crossing below a given vertex in a graph.

    Args:
     vertex -- The vertex above which crossings are counted.
     graph -- The graph in which crossings are counted.

    Returns:
     (int) -- The number of crossings below the vertex.
    """
    crossing = 0
    outgoing_edges = graph.all_outgoing_edges(vertex)
    for edge in outgoing_edges:
        head = edge.head
        tail = edge.tail

        head_index = graph.get_ordering().get(head.layer).index(head)
        tail_index = graph.get_ordering().get(tail.layer).index(tail)

        vertices_on_layer = graph.get_ordering().get(tail.layer)
        for v_index, v in enumerate(vertices_on_layer):
            incoming = graph.all_incoming_edges(v)
            for in_edge in incoming:
                in_edge_head_index = graph.get_ordering().get(in_edge.head.layer).index(in_edge.head)
                if (v_index > tail_index and in_edge_head_index < head_index) or \
                        (v_index < tail_index and in_edge_head_index > head_index):
                    crossing += 1

    return crossing


def coordinate_assignment(graph: Graph) -> Graph:
    """
        Assigns coordinates to vertices in the graph using the up and down sweep.

        Parameters:
        - graph (Graph) -- The graph to assign coordinates to.
    """
    positioned_vertices = {}
    for layer_vertices in graph.get_ordering().values():
        for i, vertex in enumerate(layer_vertices):
            positioned_vertices[vertex] = i

    for _ in range(2):
        down_sweep_assignment(graph, positioned_vertices)
        up_sweep_assignment(graph, positioned_vertices)

    for vertex, x in positioned_vertices.items():
        vertex.position = x, vertex.layer * 4

    return graph


def down_sweep_assignment(graph: Graph, vertices_position: Dict[Vertex, int]):
    """
           Assign positions to vertices in the graph using an up-sweep approach.

           Parameters:
            graph (Graph) -- The graph to assign positions to.
            vertices_position (Dict[Vertex, int]) -- Dictionary mapping vertices to their positions.
    """
    for layer in range(2, graph.get_max_layer() + 1):
        layer_vertices = graph.get_ordering().get(layer, [])

        for vertex in layer_vertices:
            incoming_positions = [vertices_position.get(e.head) for e in
                                  graph.all_incoming_edges(vertex)]

            position = median_position(incoming_positions)
            vertices_position[vertex] = adjust_vertex_position(vertex, position, vertices_position,
                                                               graph.get_ordering())


def up_sweep_assignment(graph: Graph, vertices_position: Dict[Vertex, int]):
    """
        Assign positions to vertices in the graph using an up-sweep approach.

        Parameters:
         graph (Graph) -- The graph to assign positions to.
         vertices_position (Dict[Vertex, int]) -- Dictionary mapping vertices to their positions.
    """

    # Iterate over layers of the graph in reverse order
    for layer in range(graph.get_max_layer() - 1, 0, -1):

        layer_vertices = graph.get_ordering().get(layer, [])
        for vertex in layer_vertices:
            outgoing_positions = [vertices_position.get(e.tail) for e in
                                  graph.all_outgoing_edges(vertex)]
            position = median_position(outgoing_positions)
            vertices_position[vertex] = adjust_vertex_position(vertex, position, vertices_position,
                                                               graph.get_ordering())


def adjust_vertex_position(vertex: Vertex,
                           position: int,
                           positioned_vertices: Dict[Vertex, int],
                           ordering: Dict[int, List[Vertex]]) -> int:
    """
    Adjusts the position of a vertex based on its neighbours within a layer.

    Args:
     vertex -- The vertex whose position is to be adjusted.
     position -- The initial position of the vertex.
     vertices_position -- A dictionary mapping vertices to their positions.
     ordering -- A dictionary mapping layer numbers to lists of vertices in that layer.

    Returns:
     (int) -- The adjusted position of the vertex.
    """
    vertices_on_layer = ordering.get(vertex.layer)
    leftmost = None
    rightmost = None

    # closest vertices already positioned to the left
    leftmost_list = [v for v in vertices_on_layer if
                     v in positioned_vertices and v != vertex and
                     positioned_vertices.get(v) < positioned_vertices.get(vertex)]
    if leftmost_list:
        leftmost = max(leftmost_list, key=lambda x: positioned_vertices.get(x))

    # closest vertices already positioned to the right
    rightmost_list = [v for v in vertices_on_layer if
                      v in positioned_vertices and v != vertex and
                      positioned_vertices.get(v) > positioned_vertices.get(vertex)]
    if rightmost_list:
        rightmost = min(rightmost_list, key=lambda x: positioned_vertices.get(x))

    vertex_width = 4
    vertex_offset = 4

    min_x = positioned_vertices.get(leftmost, 0) + vertex_width + vertex_offset
    max_x = positioned_vertices.get(rightmost,
                                    len(positioned_vertices)) - vertex_width

    return min(max(position, min_x), max_x)


def median_position(vertices_position: List[Vertex]) -> int:
    """
        Get the median position of a list of vertex positions.

        Parameters:
         vertices_position (List[Vertex]) -- A list of vertex positions.

        Returns:
         int -- The median position of the vertex positions.
    """
    if not vertices_position:
        return 0

    n = len(vertices_position)

    if n % 2 != 0:
        return vertices_position[n // 2]
    else:
        mid_r = vertices_position[n // 2]
        mid_l = vertices_position[(n // 2) - 1]
        return (mid_r + mid_l) // 2


def right_to_left(graph: Graph) -> None:
    """90 degrees counterclockwise rotation of the graph(graph has the bottom to top orientation)"""
    for vertex in graph.get_vertices():
        x, y = vertex.position
        vertex.position = -y, x


def left_to_right(graph: Graph) -> None:
    """90 degrees clockwise rotation of the graph(graph has the bottom to top orientation)"""
    for vertex in graph.get_vertices():
        x, y = vertex.position
        vertex.position = y, -x


def top_to_bottom(graph: Graph) -> None:
    """Reflection in the x_axis of the graph(graph has the bottom to top orientation)"""
    for vertex in graph.get_vertices():
        _, y = vertex.position
        vertex.position = _, -y


def set_orientation(graph: Graph) -> None:
    """Set the orientation of the given graph."""
    match graph.orientation:
        case "dt":
            return
        case "lr":
            left_to_right(graph)
        case "rl":
            right_to_left(graph)
        case _:
            top_to_bottom(graph)


def undo_reversed_edges(graph: Graph) -> None:
    """Undo the reversed edges of the given graph."""
    for edge in graph.edges:
        if edge.reversed:
            edge.head, edge.tail = edge.tail, edge.head
            edge.reversed = False

            # TODO: Test wrong file and wrong json format
