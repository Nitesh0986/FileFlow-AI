from pathlib import Path
from datetime import datetime
import mimetypes


def analyze_file(file_path: str) -> dict:
    """Analyze basic information about a file."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError(f"Not a file: {path}")

    stat = path.stat()

    mime_type, _ = mimetypes.guess_type(path.name)

    file_info = {
        "name": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "mime_type": mime_type or "unknown",
        "created_at": datetime.fromtimestamp(
            stat.st_ctime
        ).isoformat(),
        "modified_at": datetime.fromtimestamp(
            stat.st_mtime
        ).isoformat(),
        "path": str(path.resolve()),
    }

    return file_info


def print_file_info(file_info: dict):
    """Display analyzed file information."""

    print("\n🔎 FILE ANALYSIS")
    print("=" * 50)

    print(f"Name       : {file_info['name']}")
    print(f"Extension  : {file_info['extension']}")
    print(f"Size       : {file_info['size_bytes']} bytes")
    print(f"MIME Type  : {file_info['mime_type']}")
    print(f"Created    : {file_info['created_at']}")
    print(f"Modified   : {file_info['modified_at']}")
    print(f"Path       : {file_info['path']}")

    print("=" * 50)