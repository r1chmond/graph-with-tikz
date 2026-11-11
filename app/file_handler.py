def read(path: str) -> str:
    """
    Read and return file content

    Raises:
      OsError -- If file-related OS error occurs while reading the file.
      UnicodeDecodeError -- If content cannot be decoded while reading the file.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except (OSError, UnicodeDecodeError):
        raise


def write(path: str, content: str) -> None:
    """
    Write content to a file

    Raises:
      OSError -- If file-related OS error occurs while writing the file.
    """
    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
    except OSError:
        raise
