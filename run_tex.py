import os
import webbrowser

# os.remove("tester.txt")
os.remove("tester.aux")
# os.remove("tester.fdb_latexmk")
os.remove("tester.log")


file = os.path.join("tester.pdf")
webbrowser.open_new(file)