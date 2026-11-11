import contextlib
import os
import tempfile
from pathlib import Path

from app.exceptions import FileFormatError


def read(path: str) -> str:
    """
    Read and return file content

    Raises:
      OSError -- If file-related OS error occurs while reading the file.
      FileFormatError -- If content cannot be decoded while reading the file.
    """
    try:
        return Path(path).read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as e:
        raise FileFormatError(f"{path} is not a valid UTF-8 text") from e


def write(path: str, content: str) -> None:
    """
    Write content to a file atomically.

    Raises:
      OSError -- If file-related OS error occurs.
    """
    target = Path(path)
    fd, temp_name = tempfile.mkstemp(
        dir=target.parent, prefix=f".{target.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            file.write(content)

        os.replace(temp_name, target)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(temp_name)
        raise
