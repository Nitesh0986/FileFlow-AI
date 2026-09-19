from pathlib import Path
import re
from datetime import datetime
from typing import Dict, Optional, List


def sanitize_filename(filename: str) -> str:
    """Remove or replace invalid characters from filename."""
    
    # Replace invalid characters with underscore
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    
    # Replace multiple spaces with single space
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Replace multiple underscores with single underscore
    sanitized = re.sub(r'_+', '_', sanitized)
    
    return sanitized


def add_timestamp_prefix(filename: str, timestamp: Optional[str] = None) -> str:
    """Add timestamp prefix to filename."""
    
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    path = Path(filename)
    stem = path.stem
    suffix = path.suffix
    
    new_name = f"{timestamp}_{stem}{suffix}"
    
    return new_name


def add_counter_suffix(filename: str, counter: int) -> str:
    """Add counter suffix to filename."""
    
    path = Path(filename)
    stem = path.stem
    suffix = path.suffix
    
    new_name = f"{stem}_{counter}{suffix}"
    
    return new_name


def convert_to_lowercase(filename: str) -> str:
    """Convert filename to lowercase."""
    
    path = Path(filename)
    return path.name.lower()


def convert_to_uppercase(filename: str) -> str:
    """Convert filename to uppercase."""
    
    path = Path(filename)
    return path.name.upper()


def replace_spaces(filename: str, replacement: str = "_") -> str:
    """Replace spaces in filename with specified character."""
    
    path = Path(filename)
    stem = path.stem
    suffix = path.suffix
    
    new_stem = stem.replace(' ', replacement)
    new_name = f"{new_stem}{suffix}"
    
    return new_name


def remove_special_chars(filename: str, keep_dots: bool = True) -> str:
    """Remove special characters from filename."""
    
    path = Path(filename)
    stem = path.stem
    suffix = path.suffix
    
    # Keep only alphanumeric, spaces, and optionally dots
    if keep_dots:
        pattern = r'[^a-zA-Z0-9\s\.]'
    else:
        pattern = r'[^a-zA-Z0-9\s]'
    
    new_stem = re.sub(pattern, '', stem)
    new_name = f"{new_stem}{suffix}"
    
    return new_name


def rename_file(file_path: str, new_name: str, dry_run: bool = False) -> Dict:
    """Rename a file with safety checks."""
    
    source = Path(file_path)
    
    # Validate source file
    if not source.exists():
        raise FileNotFoundError(f"File not found: {source}")
    
    if not source.is_file():
        raise ValueError(f"Not a file: {source}")
    
    # Validate new filename
    if not new_name or not new_name.strip():
        raise ValueError("New filename cannot be empty")
    
    new_name = new_name.strip()
    
    # Check for path traversal attempts
    if '..' in new_name or new_name.startswith('/') or new_name.startswith('\\'):
        raise ValueError("Invalid filename: path traversal not allowed")
    
    # Check for absolute path attempts
    if len(new_name) > 1 and (new_name[1] == ':' or new_name.startswith('//') or new_name.startswith('\\\\')):
        raise ValueError("Invalid filename: absolute paths not allowed")
    
    # Sanitize the filename
    sanitized_name = sanitize_filename(new_name)
    
    # Preserve extension if user didn't provide one
    if '.' not in sanitized_name:
        sanitized_name = sanitized_name + source.suffix
    
    # Get the parent directory
    parent = source.parent
    
    # Create new path
    new_path = parent / sanitized_name
    
    # Check if new path already exists
    if new_path.exists() and new_path != source:
        return {
            "old_path": str(source),
            "new_path": str(new_path),
            "old_name": source.name,
            "new_name": new_path.name,
            "success": False,
            "error": "A file with this name already exists",
            "dry_run": dry_run
        }
    
    result = {
        "old_path": str(source),
        "new_path": str(new_path),
        "old_name": source.name,
        "new_name": new_path.name,
        "success": False,
        "error": None,
        "dry_run": dry_run
    }
    
    if not dry_run:
        try:
            source.rename(new_path)
            result["success"] = True
        except PermissionError:
            result["error"] = "Permission denied: cannot rename file"
        except Exception as e:
            result["error"] = str(e)
    else:
        result["success"] = True
    
    return result


def batch_rename(folder_path: str, pattern: str = None, 
                replacement: str = None, dry_run: bool = False,
                sanitize: bool = False, lowercase: bool = False) -> Dict:
    """Batch rename files in a folder."""
    
    folder = Path(folder_path)
    
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")
    
    files = list(folder.glob("*"))
    files = [f for f in files if f.is_file()]
    
    results = {
        "total_files": len(files),
        "renamed": 0,
        "failed": 0,
        "skipped": 0,
        "errors": []
    }
    
    for file_path in files:
        try:
            old_name = file_path.name
            new_name = old_name
            
            # Apply transformations
            if sanitize:
                new_name = sanitize_filename(new_name)
            
            if lowercase:
                new_name = convert_to_lowercase(new_name)
            
            if pattern and replacement:
                new_name = new_name.replace(pattern, replacement)
            
            # Skip if no change
            if new_name == old_name:
                results["skipped"] += 1
                continue
            
            result = rename_file(str(file_path), new_name, dry_run)
            
            if result["success"]:
                results["renamed"] += 1
            else:
                results["failed"] += 1
                results["errors"].append({
                    "file": str(file_path),
                    "error": result["error"]
                })
                
        except Exception as e:
            results["failed"] += 1
            results["errors"].append({
                "file": str(file_path),
                "error": str(e)
            })
    
    return results


def print_rename_results(results: Dict):
    """Display rename results."""
    
    print("\n📝 FILE RENAME RESULTS")
    print("=" * 60)
    print(f"Total files processed: {results['total_files']}")
    print(f"Renamed: {results['renamed']}")
    print(f"Failed: {results['failed']}")
    print(f"Skipped: {results['skipped']}")
    
    if results["errors"]:
        print("\n⚠️ Errors:")
        for error in results["errors"][:5]:
            print(f"   {error['file']}: {error['error']}")
        if len(results["errors"]) > 5:
            print(f"   ... and {len(results['errors']) - 5} more errors")
    
    if results.get("dry_run"):
        print("\n🔍 DRY RUN MODE - No files were actually renamed")
    
    print("=" * 60)


if __name__ == "__main__":
    # Test renamer
    print("🧪 RENAMER TEST")
    print("=" * 50)
    
    # Test individual functions
    test_names = [
        "My Document.txt",
        "file with spaces.pdf",
        "file<>with:bad/chars.jpg",
        "UPPERCASE.DOCX"
    ]
    
    print("\nSanitization test:")
    for name in test_names:
        sanitized = sanitize_filename(name)
        print(f"  {name} -> {sanitized}")
    
    print("\nLowercase test:")
    for name in test_names:
        lower = convert_to_lowercase(name)
        print(f"  {name} -> {lower}")
    
    print("\nReplace spaces test:")
    for name in test_names:
        replaced = replace_spaces(name, "_")
        print(f"  {name} -> {replaced}")
    
    print("=" * 50)
