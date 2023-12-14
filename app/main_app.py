from app.tikz_generator import TikzCodeGenerator


class MainApp:
    def __init__(self,)-> None:
        self.gen = TikzCodeGenerator("tester.json")
        
    def print_tikz_code(self):
        code = self.gen.generate_tikz_code()
        print(code)

# TODO:
# What if processes have the same?
#  Consider swapping "id" with "label"
# eg: "idx2": {"label":"walk", "type": "process"}