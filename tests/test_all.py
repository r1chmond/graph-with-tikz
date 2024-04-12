import copy
import unittest
import os
from app.file_handler import FileHandler
from app.json_parser import JSONParser
from app.tikz_generator import TikzCodeGenerator
from app.data import ParsedData
from app.graph import Vertex, Edge, Graph
from app import sugiyama


class TestFileHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.write_valid_json_file()
        self.handler = FileHandler()
        self.parsed_data = ParsedData(os.path.join("valid.json"))
        self.graph = Graph(self.parsed_data.get_parsed_data())
        self.generator = TikzCodeGenerator(self.graph)

    def tearDown(self) -> None:
        try:
            if os.path.exists("exported.tex"):
                os.remove("exported.tex")
            if os.path.exists("valid.json"):
                os.remove("valid.json")
        except OSError as e:
            print(f"Error during tearDown: {e}")

    def test_read_file_successful(self) -> None:
        data = self.handler.read("valid.json")
        self.assertIsNotNone(data)

    def test_read_nonexistent_file(self) -> None:
        data = self.handler.read("nonexistent.json")
        self.assertIsNone(data)

    def test_write_file_successful(self) -> None:
        code = self.generator.generate_tikz_code()
        self.handler.write("exported.tex", code)

        with open("exported.tex", "r") as file:
            file_content = file.read()
        self.assertIsNotNone(file_content)

    def write_valid_json_file(self) -> None:
        data = """ {
    "orientation": "td",
    "idx1": {
        "label": "start",
        "type": "terminator",
        "next": [
            {
                "id": "idx2",
                "edge": "edge"
            },
            {
                "id": "idx3",
                "edge": "desc"
            }
        ]
    },
    "idx2": {
        "label": "go",
        "type": "process",
        "next": [
            {
                "id": "idx3"
            }
            ] 
            } 
            }"""
        with open("valid.json", "w") as file:
            file.write(data)


class TestJSONParser(unittest.TestCase):

    def setUp(self) -> None:
        self.handler = FileHandler()
        self.write_invalid_json_file()
        self.write_valid_json_file()

    def tearDown(self) -> None:
        os.remove("valid.json")
        os.remove("invalid.json")

    def test_parse_json_successful(self) -> None:
        data = self.handler.read("valid.json")
        parser = JSONParser(data)
        parsed_data = parser.parse_json_data()
        self.assertIsNotNone(parsed_data)

    def test_parse_invalid_json(self) -> None:
        data = self.handler.read("invalid.json")
        parser = JSONParser(data)
        parsed_data = parser.parse_json_data()
        self.assertIsNone(parsed_data)

    def write_valid_json_file(self) -> None:
        data = """ {
                        "start": {"id": "idx1","type": "terminator", "next": {"id": "idx2"}}, 
                        "walk": {"id":"idx2", "type": "process"}
                    }"""
        with open("valid.json", "w") as file:
            file.write(data)

    def write_invalid_json_file(self) -> None:
        data = "This is not a valid json"
        with open("invalid.json", "w") as file:
            file.write(data)


class TestVertex(unittest.TestCase):

    def setUp(self) -> None:
        self.v1 = Vertex("v1", "type1", "fill1", "color1", "label1", 2, (10, 20))
        self.v2 = Vertex("v1", "type1", "fill1", "color1", "label1", 2, (10, 20))
        self.v3 = Vertex("v3", "type3", "fill3", "color3", "label3", 2, (10, 20))

    def test_vertex_init(self) -> None:
        self.assertIsInstance(self.v1, Vertex)

    def test_vertex_equality(self) -> None:
        self.assertEqual(self.v1, self.v2)
        self.assertNotEqual(self.v1, self.v3)
        self.assertNotEqual(self.v2, self.v3)

    def test_hash(self):
        self.assertEqual(hash(self.v1), hash(self.v2))
        self.assertNotEqual(hash(self.v1), hash(self.v3))


class TestEdge(unittest.TestCase):

    def setUp(self) -> None:
        self.v1 = Vertex("v1", "type1", "fill1", "color1", "label1", 2, (10, 20))
        self.v2 = Vertex("v2", "type2", "fill2", "color2", "label2", 2, (10, 20))
        self.v3 = Vertex("v3", "type3", "fill3", "color3", "label3", 2, (10, 20))
        self.edge1 = Edge(self.v1, self.v3)
        self.edge2 = Edge(self.v1, self.v3)
        self.edge3 = Edge(self.v1, self.v2)

    def test_edge_init(self) -> None:
        self.assertIsInstance(self.edge1, Edge)

    def test_edge_equality(self):
        self.assertEqual(self.edge1, self.edge2)
        self.assertNotEqual(self.edge1, self.edge3)

    def test_hash(self):
        self.assertEqual(hash(self.edge1), hash(self.edge2))
        self.assertNotEqual(hash(self.edge1), hash(self.edge3))


class TestGraph(unittest.TestCase):

    def setUp(self) -> None:
        self.handler = FileHandler()
        data = self.handler.read("json_examples/crossing_example.json")
        parser = JSONParser(data)
        self.parsed_data = parser.parse_json_data()
        self.graph = Graph(self.parsed_data)

    def test_graph_init(self):
        self.assertIsInstance(self.graph, Graph)

    def test_graph_retrieve_vertices_from_data(self) -> None:
        vertices_from_data = self.graph.get_vertices_from_data(self.parsed_data)
        self.assertIsNotNone(vertices_from_data)

    def test_graph_create_vertices(self) -> None:
        vertices = self.graph.get_vertices()
        self.assertIsInstance(vertices, list)
        self.assertIsInstance(vertices[0], Vertex)

    def test_graph_create_edges(self) -> None:
        vertices_from_data = self.graph.get_vertices_from_data(self.parsed_data)
        edges = self.graph.create_edges(vertices_from_data)
        self.assertIsInstance(edges, list)
        self.assertIsInstance(edges[0], Edge)

    def test_graph_get_number_of_vertices(self) -> None:
        num_of_vertices = self.graph.get_num_of_vertices()
        self.assertIsInstance(num_of_vertices, int)
        v = 15  # known vertices is 15
        self.assertEqual(num_of_vertices, v)

    def test_graph_get_all_outgoing_edges(self) -> None:
        vertex = self.graph.get_vertices()[0]
        edges = self.graph.all_outgoing_edges(vertex)
        self.assertIsInstance(edges, list)
        self.assertEqual(len(edges), 1)

    def test_graph_get_all_incoming_vertices(self) -> None:
        vertex = self.graph.get_vertices()[1]
        edges = self.graph.all_incoming_edges(vertex)
        self.assertIsInstance(edges, list)
        self.assertEqual(len(edges), 1)

    def test_source_vertex(self) -> None:
        vertex = self.graph.get_vertices()[0]
        edges = self.graph.all_incoming_edges(vertex)
        self.assertEqual(len(edges), 0)

    def test_sink_vertex(self) -> None:
        vertex = self.graph.get_vertex("idx13")
        edges = self.graph.all_outgoing_edges(vertex)
        self.assertEqual(len(edges), 0)

    def test_add_dummy_vertex(self) -> None:
        vertex = self.graph.add_dummy_vertex("*", "dummy", 2)
        self.assertIsInstance(vertex, Vertex)

    def test_get_existing_vertex(self) -> None:
        vertex = self.graph.get_vertex("idx14")
        self.assertEqual(vertex, self.graph.get_vertex("idx14"))

    def test_get_non_existing_vertex(self) -> None:
        vertex = self.graph.get_vertex("idx132")
        self.assertIsNone(vertex)


class TestTikzGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = FileHandler()
        data = self.handler.read("json_examples/crossing_example.json")
        parser = JSONParser(data)
        parsed_data = parser.parse_json_data()
        self.graph = Graph(parsed_data)
        self.tikz_generator = TikzCodeGenerator(self.graph)

    def test_tikz_generator_init(self):
        self.assertIsInstance(self.tikz_generator, TikzCodeGenerator)

    def test_tikz_generator_create_vertices(self) -> None:
        vertices = self.tikz_generator.create_tikz_vertices()
        self.assertIsNotNone(vertices)

    def test_tikz_generator_generate_code(self) -> None:
        code = self.tikz_generator.generate_tikz_code()
        self.assertIsNotNone(code)


class TestSugiyama(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = FileHandler()
        data = self.handler.read("json_examples/with_cycle.json")
        parser = JSONParser(data)
        self.parsed_data = parser.parse_json_data()
        self.graph = Graph(self.parsed_data)

    def test_cycle_removal(self):
        head_vertex = self.graph.get_vertex("idx3")
        edge = copy.copy(self.graph.all_outgoing_edges(head_vertex))
        sugiyama.dfs_cycle_removal(self.graph)
        new_edge = self.graph.all_outgoing_edges(head_vertex)
        self.assertNotEqual(new_edge, edge)

    def test_layer_assignment(self):
        sugiyama.longest_path_layer_assigment(self.graph)
        vertex = self.graph.get_vertex("idx1")
        self.assertEqual(vertex.layer, 1)

    def test_add_dummy_vertex(self):
        num_of_vertices = self.graph.get_num_of_vertices()
        sugiyama.dfs_cycle_removal(self.graph)
        sugiyama.longest_path_layer_assigment(self.graph)
        sugiyama.add_dummy_vertices(self.graph)
        self.assertNotEqual(num_of_vertices, self.graph.get_num_of_vertices())

    def test_init_ordering(self):
        sugiyama.dfs_cycle_removal(self.graph)
        sugiyama.longest_path_layer_assigment(self.graph)
        sugiyama.add_dummy_vertices(self.graph)
        sugiyama.init_ordering(self.graph)
        ordering = self.graph.get_ordering()
        self.assertIsInstance(ordering.get(1)[0], Vertex)

    def test_cross_reduction(self):
        sugiyama.dfs_cycle_removal(self.graph)
        sugiyama.longest_path_layer_assigment(self.graph)
        sugiyama.add_dummy_vertices(self.graph)
        sugiyama.init_ordering(self.graph)
        ordering = copy.copy(self.graph.get_ordering())
        self.assertIsInstance(ordering.get(1)[0], Vertex)
        sugiyama.cross_reduction(self.graph)
        self.assertNotEqual(ordering, self.graph.get_ordering())

    def test_x_coordinates(self):
        sugiyama.dfs_cycle_removal(self.graph)
        sugiyama.longest_path_layer_assigment(self.graph)
        sugiyama.add_dummy_vertices(self.graph)
        sugiyama.init_ordering(self.graph)
        sugiyama.cross_reduction(self.graph)
        sugiyama.coordinate_assignment(self.graph)
        vertex = self.graph.get_vertex("idx1")
        self.assertNotEqual(vertex.position, (0,0))




