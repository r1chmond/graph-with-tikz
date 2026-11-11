import os
import tempfile
from pathlib import Path

from app.exceptions import FileFormatError


def read(path: str) -> str:
    """
    Read and return file content

    Raises:
      OsError -- If file-related OS error occurs while reading the file.
      UnicodeDecodeError -- If content cannot be decoded while reading the file.
    """
    try:
        return Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        raise FileFormatError() from e


def write(path: str, content: str) -> None:
    """
    Write content to a file safely

    Raises:
      OSError -- If file-related OS error occurs while writing the file.
    """
    path_obj = Path(path)
    fd, temp_name = tempfile.mkstemp(dir=path_obj.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            file.write(content)

        os.replace(temp_name, path_obj)
    except Exception:
        os.unlink(temp_name)
        raise
