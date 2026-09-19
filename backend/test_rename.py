"""
FileFlow-AI Rename Module Test Script

Tests the safe rename functionality with various edge cases.
"""

from pathlib import Path
import shutil
from renamer import rename_file

def test_rename():
    """Test the rename functionality with safety checks."""
    
    print("=" * 60)
    print("🧪 FILEFLOW-AI RENAME TEST")
    print("=" * 60)
    
    # Setup paths
    test_folder = Path(__file__).resolve().parent.parent / "sample_files"
    
    # Test Case 1: Normal rename
    print("\n📝 Test Case 1: Normal rename")
    test_file = test_folder / "rename_test.txt"
    if test_file.exists():
        try:
            result = rename_file(str(test_file), "renamed_test.txt", dry_run=True)
            print(f"  Result: {result['success']}")
            print(f"  Old: {result['old_name']}")
            print(f"  New: {result['new_name']}")
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print("  Skipped: test file not found")
    
    # Test Case 2: Rename to existing filename
    print("\n📝 Test Case 2: Rename to existing filename")
    existing_file = test_folder / "existing_name.txt"
    if test_file.exists():
        try:
            result = rename_file(str(test_file), "existing_name.txt", dry_run=True)
            print(f"  Result: {result['success']}")
            if not result['success']:
                print(f"  Error: {result['error']}")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Test Case 3: Empty filename
    print("\n📝 Test Case 3: Empty filename")
    if test_file.exists():
        try:
            result = rename_file(str(test_file), "", dry_run=True)
            print(f"  Result: {result['success']}")
        except ValueError as e:
            print(f"  Expected error: {e}")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Test Case 4: Invalid filename
    print("\n📝 Test Case 4: Invalid filename")
    if test_file.exists():
        try:
            result = rename_file(str(test_file), "test<>file.txt", dry_run=True)
            print(f"  Result: {result['success']}")
            print(f"  Sanitized: {result['new_name']}")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Test Case 5: Non-existing source
    print("\n📝 Test Case 5: Non-existing source")
    try:
        result = rename_file(str(test_folder / "nonexistent.txt"), "new_name.txt", dry_run=True)
        print(f"  Result: {result['success']}")
    except FileNotFoundError as e:
        print(f"  Expected error: {e}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test Case 6: Directory supplied as source
    print("\n📝 Test Case 6: Directory supplied as source")
    try:
        result = rename_file(str(test_folder), "new_name.txt", dry_run=True)
        print(f"  Result: {result['success']}")
    except ValueError as e:
        print(f"  Expected error: {e}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test Case 7: Path traversal attempt
    print("\n📝 Test Case 7: Path traversal attempt")
    if test_file.exists():
        try:
            result = rename_file(str(test_file), "../malicious.txt", dry_run=True)
            print(f"  Result: {result['success']}")
        except ValueError as e:
            print(f"  Expected error: {e}")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Test Case 8: Extension preservation
    print("\n📝 Test Case 8: Extension preservation")
    if test_file.exists():
        try:
            result = rename_file(str(test_file), "final_report", dry_run=True)
            print(f"  Result: {result['success']}")
            print(f"  New name: {result['new_name']}")
            print(f"  Extension preserved: {result['new_name'].endswith('.txt')}")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ RENAME TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    test_rename()
