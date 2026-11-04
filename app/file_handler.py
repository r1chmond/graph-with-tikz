from app.custom_log import log


class FileHandler:

    def read(self, path: str) -> str:
        """
        Read and return file content

        Raises:
          IOError -- If file-related OS error occurs while reading the file.
        """
        try:
            with open(path, "r") as file:
                return file.read()
        except IOError:
            log.exception("Error occurred while reading file.")
            raise

    def write(self, path: str, content: str) -> None:
        """
        Write content to a file

        Raises:
          IOError -- If file-related OS error occurs while writing the file.
        """
        try:
            with open(path, "w") as file:
                log.debug("============== open run ==============")
                file.write(content)
        except IOError:
            log.exception("Error occurred while writing file.")
            raise
