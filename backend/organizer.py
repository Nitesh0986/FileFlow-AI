from pathlib import Path
import shutil
from typing import Dict, Optional
from backend.classifier import classify_file, get_category_folder, FILE_CATEGORIES


def organize_file(file_path: str, target_base: str, dry_run: bool = False) -> Dict:
    """Move a file to its category folder."""
    
    source = Path(file_path)
    
    if not source.exists():
        raise FileNotFoundError(f"File not found: {source}")
    
    if not source.is_file():
        raise ValueError(f"Not a file: {source}")
    
    # Get file info for classification
    file_info = {
        "name": source.name,
        "extension": source.suffix,
    }
    
    # Classify the file
    category = classify_file(file_info)
    category_folder = get_category_folder(category)
    
    # Create target directory path
    target_base_path = Path(target_base)
    target_dir = target_base_path / category_folder
    
    # Create target directory if it doesn't exist
    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
    
    # Target file path
    target_file = target_dir / source.name
    
    # Check if target file already exists
    if target_file.exists():
        # Add a suffix to avoid overwriting
        counter = 1
        while target_file.exists():
            stem = source.stem
            suffix = source.suffix
            target_file = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1
    
    # Move the file
    old_path = str(source)
    new_path = str(target_file)
    
    result = {
        "source": old_path,
        "destination": new_path,
        "category": category,
        "success": False,
        "error": None,
        "dry_run": dry_run
    }
    
    if not dry_run:
        try:
            shutil.move(str(source), str(target_file))
            result["success"] = True
        except Exception as e:
            result["error"] = str(e)
    else:
        result["success"] = True  # Dry run always succeeds
    
    return result


def organize_folder(source_folder: str, target_base: str, 
                   dry_run: bool = False, recursive: bool = True) -> Dict:
    """Organize all files in a folder into category subfolders."""
    
    source = Path(source_folder)
    
    if not source.exists():
        raise FileNotFoundError(f"Folder not found: {source}")
    
    if not source.is_dir():
        raise NotADirectoryError(f"Not a directory: {source}")
    
    # Get all files
    if recursive:
        files = list(source.rglob("*"))
    else:
        files = list(source.glob("*"))
    
    # Filter out database files and temporary files
    files = [f for f in files if f.is_file() and f.suffix not in ['.db', '.db-journal', '.tmp', '.temp']]
    
    results = {
        "total_files": len(files),
        "organized": 0,
        "failed": 0,
        "skipped": 0,
        "by_category": {},
        "errors": []
    }
    
    for file_path in files:
        try:
            # Skip files that are already in a category folder
            relative_path = file_path.relative_to(source)
            if len(relative_path.parts) > 1:
                results["skipped"] += 1
                continue
            
            result = organize_file(str(file_path), target_base, dry_run)
            
            if result["success"]:
                results["organized"] += 1
                
                category = result["category"]
                if category not in results["by_category"]:
                    results["by_category"][category] = 0
                results["by_category"][category] += 1
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


def print_organization_results(results: Dict):
    """Display organization results."""
    
    print("\n📁 FILE ORGANIZATION RESULTS")
    print("=" * 60)
    print(f"Total files processed: {results['total_files']}")
    print(f"Organized: {results['organized']}")
    print(f"Failed: {results['failed']}")
    print(f"Skipped: {results['skipped']}")
    
    if results["by_category"]:
        print("\n📂 Files by category:")
        for category, count in results["by_category"].items():
            print(f"   {category}: {count}")
    
    if results["errors"]:
        print("\n⚠️ Errors:")
        for error in results["errors"][:5]:  # Show first 5 errors
            print(f"   {error['file']}: {error['error']}")
        if len(results["errors"]) > 5:
            print(f"   ... and {len(results['errors']) - 5} more errors")
    
    if results.get("dry_run"):
        print("\n🔍 DRY RUN MODE - No files were actually moved")
    
    print("=" * 60)


def create_category_structure(base_path: str):
    """Create all category folders in the base directory."""
    
    from classifier import FILE_CATEGORIES
    
    base = Path(base_path)
    
    for category in FILE_CATEGORIES.keys():
        if category == "Other":
            continue
        
        folder_name = get_category_folder(category)
        folder_path = base / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ Created folder: {folder_name}")


if __name__ == "__main__":
    # Test organizer
    print("🧪 ORGANIZER TEST")
    print("=" * 50)
    
    # Test with sample_files
    sample_folder = Path(__file__).resolve().parent.parent / "sample_files"
    organized_folder = Path(__file__).resolve().parent.parent / "organized"
    
    if sample_folder.exists():
        print(f"Source folder: {sample_folder}")
        print(f"Target folder: {organized_folder}")
        
        # Dry run first
        print("\n🔍 DRY RUN")
        results = organize_folder(
            str(sample_folder), 
            str(organized_folder), 
            dry_run=True,
            recursive=False
        )
        print_organization_results(results)
        
    else:
        print("Sample files folder not found for testing")
    
    print("=" * 50)
