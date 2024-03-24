

class FileHandler:
    
    def read(self, path: str) -> str:
        '''
        Read file content
        Returns:
        str -- The content of the file as a string, or None if an error occurs
        Raises:
        FileNotFoundError -- If the file specified by `path` does not exist.
        IOError -- If an error occurs while reading the file.
        '''
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
        '''
        Write content to a file
        Raises:
        PermissionError -- If the user does not have permission to write to the file.
        Exception -- For any other unexpected error while accessing or writing to the file.
        '''
        try:
            with open(path, "w+") as file:
                file.write(content)
        except PermissionError as e:
            print(f"Permission error while accessing file: {path} - {e}")
        except Exception as e:
            print(f"An error occurred while accessing file {path}: {e}")