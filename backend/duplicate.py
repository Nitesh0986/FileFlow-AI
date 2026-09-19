from pathlib import Path
import hashlib
from typing import Dict, List, Tuple, Optional


def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate hash of a file for duplicate detection."""
    
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")
    
    # Select hash algorithm
    if algorithm == "md5":
        hash_func = hashlib.md5()
    elif algorithm == "sha1":
        hash_func = hashlib.sha1()
    elif algorithm == "sha256":
        hash_func = hashlib.sha256()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    # Read file in chunks to handle large files
    chunk_size = 8192
    with open(path, 'rb') as f:
        while chunk := f.read(chunk_size):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()


def find_duplicates(folder_path: str, algorithm: str = "sha256") -> Dict[str, List[str]]:
    """Find all duplicate files in a folder."""
    
    folder = Path(folder_path)
    
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")
    
    # Dictionary to store hash -> list of file paths
    hash_map = {}
    
    # Walk through all files in the folder
    for file_path in folder.rglob("*"):
        if file_path.is_file():
            try:
                file_hash = calculate_file_hash(str(file_path), algorithm)
                
                if file_hash not in hash_map:
                    hash_map[file_hash] = []
                
                hash_map[file_hash].append(str(file_path))
                
            except Exception as e:
                print(f"⚠️ Error hashing {file_path}: {e}")
    
    # Filter to only include duplicates (hashes with >1 file)
    duplicates = {
        hash_val: paths 
        for hash_val, paths in hash_map.items() 
        if len(paths) > 1
    }
    
    return duplicates


def get_duplicate_groups(duplicates: Dict[str, List[str]]) -> List[Dict]:
    """Convert duplicate hash map to structured groups."""
    
    groups = []
    
    for hash_val, paths in duplicates.items():
        # Sort paths to have consistent ordering
        sorted_paths = sorted(paths)
        
        # First file is considered the original
        original = sorted_paths[0]
        duplicate_files = sorted_paths[1:]
        
        groups.append({
            "hash": hash_val,
            "original": original,
            "duplicates": duplicate_files,
            "count": len(paths)
        })
    
    # Sort by count (most duplicates first)
    groups.sort(key=lambda x: x["count"], reverse=True)
    
    return groups


def print_duplicates(duplicate_groups: List[Dict]):
    """Display duplicate file information."""
    
    if not duplicate_groups:
        print("\n✅ No duplicates found!")
        return
    
    print("\n🔍 DUPLICATE FILES FOUND")
    print("=" * 60)
    
    total_duplicates = 0
    total_space = 0
    
    for i, group in enumerate(duplicate_groups, 1):
        print(f"\n📦 Group {i}: {group['count']} files")
        print(f"   Hash: {group['hash'][:16]}...")
        print(f"   Original: {group['original']}")
        
        for dup in group['duplicates']:
            dup_size = Path(dup).stat().st_size
            total_space += dup_size
            total_duplicates += 1
            print(f"   Duplicate: {dup}")
    
    print("\n" + "=" * 60)
    print(f"Total duplicate groups: {len(duplicate_groups)}")
    print(f"Total duplicate files: {total_duplicates}")
    print(f"Potential space savings: {total_space:,} bytes ({total_space / (1024*1024):.2f} MB)")
    print("=" * 60)


def quick_duplicate_check(file_path: str, existing_hashes: Dict[str, str]) -> Optional[str]:
    """Check if a file is a duplicate based on existing hash map."""
    
    try:
        file_hash = calculate_file_hash(file_path)
        
        if file_hash in existing_hashes:
            return existing_hashes[file_hash]
        
        return None
        
    except Exception as e:
        print(f"⚠️ Error checking duplicate: {e}")
        return None


if __name__ == "__main__":
    # Test duplicate detection
    print("🧪 DUPLICATE DETECTOR TEST")
    print("=" * 50)
    
    # Test hash calculation
    test_file = Path(__file__).resolve().parent.parent / "sample_files"
    
    if test_file.exists():
        print(f"Scanning folder: {test_file}")
        duplicates = find_duplicates(str(test_file))
        duplicate_groups = get_duplicate_groups(duplicates)
        print_duplicates(duplicate_groups)
    else:
        print("Sample files folder not found for testing")
    
    print("=" * 50)
