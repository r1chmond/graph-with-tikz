

class FileHandler:
    
    
    def read(self, path: str) -> str:
        try:
            with open(path, "r") as file:
                json_content = file.read()
                return json_content
        except FileNotFoundError as e:
            print(f"File not found!!! \n {e}")
            return None
        except IOError:
            print(f"An error occurred while reading file!.")
            return None
    
    def write(self, path: str, content: str) -> None:
        try:
            with open(path, "w") as file:
                file.write(content)
        except PermissionError as e:
            print(f"Permission error while accessing file: {path} - {e}")
        except Exception as e:
            print(f"An error occurred while accessing file {path}: {e}")