from typing import Dict, OrderedDict
from app.graph import Graph


class TikzCodeGenerator:
    def __init__(self, graph: Graph) -> None:
        """
        Initialise TikzCodeGenerator object
        Args:
            graph (Graph) -- graph to generate tikz code from.
        """
        self.graph: Graph = graph

    def create_tikz_vertices(self, ) -> OrderedDict[str, str]:
        """
        Create TikZ vertex representations based on input data.
        Returns:
            OrderedDict[str, str]: Ordered dictionary containing vertex IDs as keys and TikZ node representations as values.
        """
        vertices_representation = OrderedDict()
        for vertex in self.graph.get_vertices():
            vertex_id = vertex.vertex_id
            label = vertex.label
            node_type = vertex.vertex_type
            text_color = vertex.font_color
            shape_color = vertex.shape_color
            fill_color = vertex.shape_fill
            position = vertex.position
            if vertex.is_dummy:
                node_representation = f"\\node[{node_type},draw= none, text={text_color},fill={fill_color}!50]({vertex_id}) at {position} {{{label}}}"
            else:
                node_representation = f"\\node[{node_type},draw= {shape_color}, text={text_color},fill={fill_color}!50]({vertex_id}) at {position} {{{label}}}"
            vertices_representation[vertex_id] = node_representation
        return vertices_representation

    def generate_tikz_code(self) -> str:
        """
        Generates tikz code
        Returns:
            str: tikz code to be exported
        """
        template = self.template()
        all_nodes = self.create_tikz_vertices()
        code = (
                template["preamble"] + "\n" +
                template["start_tikz"] + self.get_shape_template() + "\n"
        )
        # Generate code for nodes first
        code += f"% Create nodes \n"
        for _, representation in all_nodes.items():
            code += f"{representation}; \n"

        code += f"% Connect nodes \n"

        # Generate code for connecting nodes
        for edge in self.graph.edges:
            # Handle different cases of edges
            if edge.head == edge.tail:
                code += f"\\draw[-{{Latex}}] ({edge.head.vertex_id}) edge [loop above] (); \n"
                continue

            if edge.head.is_dummy and edge.tail.is_dummy:
                code += f"\\draw ({edge.head.vertex_id}.center) -- ({edge.tail.vertex_id}.center); \n"
            elif edge.head.is_dummy:
                code += f"\\draw[-{{Latex}}] ({edge.head.vertex_id}.center) -- ({edge.tail.vertex_id}); \n"
            elif edge.tail.is_dummy:
                code += f"\\draw ({edge.head.vertex_id}) -- ({edge.tail.vertex_id}.center); \n"
            else:
                code += f"\\draw[-{{Latex}}] ({edge.head.vertex_id}) -- ({edge.tail.vertex_id}); \n"

        code += template["end"]

        return code

    def template(self) -> Dict[str, str]:
        """
        Generate a template for TikZ code.
        Returns:
            Dict[str, str]: Dictionary containing TikZ code template components.
        """
        # Define the preamble containing necessary TikZ libraries
        preamble = (r"\usetikzlibrary{graphs,positioning,quotes,shapes.geometric,arrows.meta}"
                    "\n"
                    )
        return {
            "preamble": preamble,
            "start_tikz": r"\begin{tikzpicture}",
            "end": r"\end{tikzpicture}"
        }

    def get_shape_template(self) -> str:
        """
        get all shape templates
        Returns:
            str -- String representing the shape templates for different vertex types in TikZ.
        """
        template = (
            r"[nodes={}, io/.style={{trapezium,thick,trapezium left angle=70, trapezium right angle=110, "
            r"minimum width=3cm, minimum height=1cm}}, decision/.style={{diamond, thick,minimum width=3cm, "
            r"minimum height=1cm}}, terminator/.style={{rectangle, rounded corners=3ex, thick, minimum width=3cm, "
            r"minimum height=1cm}}, process/.style={{rectangle, thick, minimum width=3cm, minimum height=1cm}},"
            r"dummy/.style={{rectangle, minimum size=1mm, text opacity=0}}]"
        )
        return template
