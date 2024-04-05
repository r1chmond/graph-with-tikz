from collections import OrderedDict
from collections import deque
from typing import Dict,List, Tuple, Any
import copy

class Vertex:
    def __init__(self, vertex_id: str,
                 vertex_type: str, 
                 shape_fill: str,
                 shape_color: str, 
                 font_color: str,
                 label: str="", 
                 layer: int = 0,
                 position: Tuple[int,int] = (0,0)) -> None:
        '''
        Initialise a Vertex object
        Args:
            vertex_id (str) -- The unique identifier of the vertex.
            vertex_type (str) -- The type of the vertex(eg: process, terminal, etc).
            shape_fill (str) -- The fill color of the vertex shape.
            shape_color (str) -- The outline color of the vertex shape.
            font_color (str) -- The color of the font used to label the vertex.
            label (str, optional) -- The label of the vertex (default "").
            layer (int, optional) -- The layer of the vertex (default 0).
            position (Tuple[int,int], optional) -- The position of the vertex (default (0,0)).
        '''
        self.vertex_id = vertex_id
        self.label = label
        self.layer = layer
        self.vertex_type = vertex_type
        self.shape_fill = shape_fill
        self.shape_color = shape_color
        self.font_color = font_color
        self.is_source = False
        self.is_sink = False
        self.is_dummy = False
        self.position = position
    
    def __eq__(self, other: object) -> bool:
        '''Return True if both instances are equal, False if otherwise'''
        return (self.vertex_id == other.vertex_id and
                self.label == other.label and
                self.layer == other.layer and
                self.vertex_type == other.vertex_type and
                self.shape_fill == other.shape_fill and
                self.shape_color == other.shape_color and 
                self.font_color == other.font_color and 
                self.position == other.position and
                self.is_sink == other.is_sink and 
                self.is_dummy == other.is_dummy and
                self.is_source == other.is_source)
        
    def __ne__(self, other: object) -> bool:
        '''Return True if both instances are not equal, False if otherwise'''
        return not self == other
    
    def __hash__(self) -> int:
        '''Return the hash value of the Vertex object'''
        return hash((self.vertex_id,self.label, self.layer, self.vertex_type,self.position,self.shape_fill,self.shape_color, self.is_source, self.is_sink, self.is_dummy))
    
    def __repr__(self) -> str:
        '''Return a str representation of the Vertex object'''
        symbol = ""
        if self.is_source:
            symbol = "+"
        elif self.is_sink:
            symbol = "-"
        return f"{symbol}{self.label}_{self.layer} pos({self.position})"
    
    
class Edge:
    def __init__(self, head: Vertex, tail: Vertex, weight: int = 1, edge_color: str = "black") -> None:
        '''
        Initialize an Edge object.

        Args:
            head (Vertex) -- The head vertex of the edge.
            tail (Vertex) -- The tail vertex of the edge.
            weight (int, optional) -- The weight of the edge (default 1).
            edge_color (str, optional) -- The color of the edge (default "black").
        '''
        self.head = head
        self.tail = tail
        self.weight = weight
        self.edge_color = edge_color
        self.reversed = False 
        
    
    def __eq__(self, other: object) -> bool:
        '''Return True if both instances are equal, False if otherwise'''
        if isinstance(other, Edge):
            return self.head == other.head and \
                    self.tail == other.tail and \
                    self.weight == other.weight and \
                    self.reversed == other.reversed
        return False
    
    def __ne__(self, other: object) -> bool:
        '''Return True if both instances are not equal, False if otherwise'''
        return not self == other
          
    def __hash__(self) -> int:
        '''Return the hash value of the Edge object'''
        return hash((self.head, self.tail, self.weight))
        
    def __repr__(self) -> str:
        '''Return a str representation of the Vertex object'''
        return f"Edge({self.head} --{self.weight}-> {self.tail}) [is_back_edge = {self.reversed}]"
        
class Graph:
    def __init__(self, data: Dict[str,Dict[str,str]]) -> None:
        '''
        Initialize a Graph object.

        Args:
            data (Dict[str,Dict[str,str]]) -- The parsed data to create the graph from.
        '''
        self._parsed_data = data
        self.vertices: List[Vertex] = []
        self.orientation: str = ""
        self.font_color: str = ""
        self.shape_color: str = ""
        self.shape_fill: str = ""
        self.edge_color: str = ""
        self.set_graph_styles()
        self.edges = self.create_edges(self.get_vertices_from_data(self._parsed_data))
        self.ordering: Dict[int, List[Vertex]] = {}
        
    
    def get_vertices_from_data(self, data: Dict[str,Dict[str,str]]) -> Dict[str,Dict[str,str]]:
        '''
        Extract vertices data from the parsed data.
        Args:
            data (Dict[str,Dict[str,str]]) -- The parsed data containing information about vertices.
        Returns:
            Dict[str,Dict[str,str]] -- A dictionary containing only the vertices data, with their id as key.
        '''
        data_vertices = {key: value for key, value in data.items() if key != 'orientation' and key != 'chartStyle'}
        all_vertices = {}
        for details in data_vertices.values():
            next_vertices = details.get("next", [])
            for next_dict in next_vertices:
                all_vertices[next_dict.get("id")] = {}
                
        for vertex_id in all_vertices:
            if vertex_id not in data_vertices:
                data_vertices[vertex_id] = {}
        return data_vertices
    
    def update_vertices(self) -> None:
        '''Update the vertices list based on the edges.'''
        for edge in self.edges:
             self.vertices.append(edge.head)
             self.vertices.append(edge.tail)
    
    def get_num_of_vertices(self) -> int:
        return len(self.vertices)
    
    def add_edge(self,head: Vertex, tail: Vertex, weight: int = 1, is_reversed: bool = False) -> None:
        '''
        Add a new edge to the graph.

        Args:
            head (Vertex) -- The head vertex of the edge.
            tail (Vertex) -- The tail vertex of the edge.
            weight (int, optional) -- The weight of the edge (default 1).
            is_reversed (bool, optional) -- Whether the edge is reversed (default False).
        '''
        new_edge = Edge(head,tail,weight)
        new_edge.reversed = is_reversed
        self.edges.append(new_edge)
        self.update_vertices()
        
    def add_dummy_vertex(self,vertex_id: str, label: str,layer: int, font_color: str = "white") -> Vertex:
        vertex = Vertex(vertex_id,"dummy","white","black",font_color,label,layer)
        return vertex
    
    def create_edges(self, data_vertices: Dict[str,Dict[str,str] ]) -> List[Edge]:
        '''
        Create edges between vertices based on the provided data.
        Args:
            data_vertices (Dict[str,Dict[str,str]]) -- Dictionary containing vertex IDs as keys and details as values.
        Returns:
            List[Edge] -- List of edges created between vertices.
        '''
        vertex_mapping = self.create_vertices(data_vertices)
        edges: List[Edge] = []
        count = 0 #ensure unique default vertices
        for vertex_id, detail in data_vertices.items():
            next_vertices = detail.get("next",[])                                                    
            connected_nodes = [(node.get("id",""), node.get("edge",""))  for node in next_vertices]
            head = vertex_mapping.get(vertex_id)
            # if head not in vertex_mapping:
            #     vertex_mapping[head.vertex_id] = head
            edges.extend([Edge(head,vertex_mapping[next_id]) for next_id,_ in connected_nodes])
            count += 1
        self.remove_duplicates(edges)
        return edges
    
    def create_vertices(self, data_vertices: Dict[str,Dict[str,str]]) -> Dict[str,Vertex]:
        '''
        Create vertices based on the provided data.
        Args:
            data_vertices (Dict[str,Dict[str,str]]) -- Dictionary containing vertex IDs as keys and details as values. 
        Returns:
            Dict[str,Vertex] -- Dictionary containing vertex IDs as keys and is corresponding Vertex as values. 
        '''
        #TODO:if user create next but not the vertex.. create default terminator
        vertex_mapping = {}
        
        for vertex_id,detail in data_vertices.items():
            label = detail.get("label", "default")
            vertex_type = detail.get("type", "process")
            # style = self._parsed_data.get("chartStyle",{})
            text_color = detail.get("fontColor",self.font_color)
            # edge_color = detail.get("edgeColor")
            # subgraph = detail.get("subgraph")
            fill_color = detail.get("shapeFill",self.shape_fill) 
            shape_color = detail.get("shapeColor",self.shape_color)
            vertex = Vertex(vertex_id, vertex_type, fill_color, shape_color, text_color, label)
            vertex_mapping[vertex_id] = vertex
            self.vertices.append(vertex)
        return vertex_mapping

    def add_vertex(self, vertex_id: str) -> Vertex:
        new_vertex = Vertex(vertex_id, "terminator", "white", "black", "black", "default")   
        self.get_vertices().append(new_vertex)
        return new_vertex
    
    def set_graph_styles(self,) -> None:
        self.orientation = self._parsed_data.get("orientation", "td")
        self.font_color = self._parsed_data.get("fontColor", "black")
        self.shape_color = self._parsed_data.get("shapeColor", "black")
        self.shape_fill = self._parsed_data.get("shapeFill", "white")
        self.edge_color = self._parsed_data.get("edgeColor", "black")
    
    def all_outgoing_edges(self, vertex: Vertex) -> List[Edge]:
        '''
        Get all outgoing edges of a given vertex.
        Args:
            vertex (Vertex) -- The vertex whose outgoing edges are to be retrieved.
        Returns:
            List[Edge] -- List of outgoing edges from the given vertex
        '''
        return [edge for edge in self.edges if edge.head == vertex]  
    

    def all_incoming_edges(self, vertex: Vertex) -> List[Edge]:
        '''
        Get all incoming edges of a given vertex.
        Args:
            vertex (Vertex) -- The vertex whose incoming edges are to be retrieved.
        Returns:
            List[Edge] -- List of incoming edges from the given vertex
        '''   
        return [edge for edge in self.edges if edge.tail == vertex]
    
    

    def get_vertex(self, vertex_id: str) -> Vertex:
        '''
        Get a vertex by its ID.
        Args:
            vertex_id (str) -- The ID of the vertex to retrieve.
        Returns:
            Vertex or None -- The vertex with the given ID if found, otherwise None.
        '''
        for v in self.vertices:
            if vertex_id == v.vertex_id:
                return v
        return None
    
    def get_vertices(self) -> List[Vertex]:
        return self.vertices


    def get_source_vertices(self) -> List[Vertex]:
        '''
        Get vertices with no incoming edges.
        Returns:
            List[Vertex] -- List of source vertices.
        '''
        source_vertices = []
        for vertex in self.vertices:
            if len(self.all_incoming_edges(vertex)) == 0:
                vertex.is_source = True
                source_vertices.append(vertex)
        return source_vertices
    
    def get_max_layer(self,) -> int:
        '''
        Get the maximum layer among all vertices.
        Returns:
            int -- The maximum layer value found among all vertices
        '''
        max_layer = 0
        for vertex in self.vertices:
            max_layer = max(max_layer, vertex.layer)  
        return max_layer
    
    def get_ordering(self) -> Dict[int, List[Vertex]]:
        return self.ordering
    
    def update_ordering(self, new_ordering: Dict[int, List[Vertex]]) -> None:
        self.ordering = new_ordering
    
    def remove_duplicates(self, elements: List[Any]) -> None:
        seen = OrderedDict()
        for element in elements:
            if element not in seen:
                seen[element] = None
            
        elements.clear()
        elements.extend(list(seen.keys()))
        
    
    #TODO: delete below
    def print_graph(self):
        for edge in self.edges:
            print(edge)
    
