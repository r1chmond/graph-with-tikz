
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
    
    def write(self, path: str, filename: str) -> None:
        pass