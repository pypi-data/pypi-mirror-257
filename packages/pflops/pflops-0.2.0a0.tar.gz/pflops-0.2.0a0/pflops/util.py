from io import IOBase
import os
from typing import Iterable, List, Optional, TypeVar

from cuid2 import cuid_wrapper

T = TypeVar("T")


def cuid_generator(prefix: Optional[str]) -> str:
    cuid = cuid_wrapper()()
    return f"{prefix}_{cuid}" if prefix else cuid


def get_file_size(file: IOBase) -> int:
    """
    Return the size of the file in bytes.
    It resets the file pointer to the beginning of the file.
    """
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size


def format_size(bytes: int) -> str:
    """
    Return a human-readable size string.
    """
    for unit in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
        if bytes < 1000:
            return f"{bytes:.2f} {unit}"
        bytes /= 1000
    return f"{bytes:.2f} YB"


def chunks(lst: List[T], n: int) -> Iterable[List[T]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
