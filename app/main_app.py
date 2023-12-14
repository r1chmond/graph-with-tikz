from app.tikz_generator import TikzCodeGenerator
from app.data import ParsedData

class MainApp:
    def __init__(self,path: str)-> None:
        self._parsed_data = ParsedData(path)
        self.gen = TikzCodeGenerator(self._parsed_data.get_parsed_data())
        
    def print_tikz_code(self):
        code = self.gen.generate_tikz_code()
        print(code)

# TODO:
# What if processes have the same?
#  Consider swapping "id" with "label"
# eg: "idx2": {"label":"walk", "type": "process"}