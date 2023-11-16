from code_generator import TikzCodeGenerator

gen = TikzCodeGenerator("tester.json")

code = gen.generate_tikz_code()

print(code)

# TODO:
# What if processes have the same?
#  Consider swapping "id" with "label"
# eg: "idx2": {"label":"walk", "type": "process"}