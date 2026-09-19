"""
FileFlow-AI Pipeline Test Script

Tests the complete file processing pipeline without touching real user files.
All tests are performed within sample_files/ directory.
"""

from pathlib import Path
import shutil
from analyzer import analyze_file
from classifier import classify_file, get_category_folder
from renamer import sanitize_filename, replace_spaces
from duplicate import calculate_file_hash
from organizer import organize_file
from database import FileDatabase

def test_pipeline():
    """Test the complete FileFlow-AI pipeline."""
    
    print("=" * 60)
    print("🧪 FILEFLOW-AI PIPELINE TEST")
    print("=" * 60)
    
    # Setup paths
    base_folder = Path(__file__).resolve().parent.parent / "sample_files"
    test_folder = base_folder / "test_pipeline"
    organized_folder = base_folder / "test_organized"
    db_path = test_folder / "test_fileflow.db"
    
    # Clean up previous test
    if test_folder.exists():
        shutil.rmtree(test_folder)
    if organized_folder.exists():
        shutil.rmtree(organized_folder)
    
    # Create test directories
    test_folder.mkdir(parents=True, exist_ok=True)
    organized_folder.mkdir(parents=True, exist_ok=True)
    
    # Create test file
    test_file = test_folder / "test_resume.txt"
    test_file.write_text("""
RESUME

Name: Nitesh Barnwal

Education:
B.Tech Computer Science and Engineering

Skills:
Python
C++
JavaScript
React
Machine Learning

Experience:
Software Development Intern
""")
    
    print(f"\n✓ Created test file: {test_file}")
    
    # Step 1: Analyze
    print("\n📊 Step 1: Analyze")
    file_info = analyze_file(str(test_file))
    print(f"  Name: {file_info['name']}")
    print(f"  Size: {file_info['size_bytes']} bytes")
    print(f"  MIME: {file_info['mime_type']}")
    
    # Step 2: Classify
    print("\n📂 Step 2: Classify")
    category = classify_file(file_info)
    folder = get_category_folder(category)
    print(f"  Category: {category}")
    print(f"  Folder: {folder}")
    
    # Step 3: Smart Rename
    print("\n✏️ Step 3: Smart Rename")
    smart_name = sanitize_filename(file_info['name'])
    smart_name = replace_spaces(smart_name, "_")
    print(f"  Original: {file_info['name']}")
    print(f"  Smart: {smart_name}")
    
    # Step 4: Hash
    print("\n🔐 Step 4: Calculate Hash")
    file_hash = calculate_file_hash(str(test_file))
    print(f"  Hash: {file_hash[:16]}...")
    
    # Step 5: Database
    print("\n💾 Step 5: Database")
    db = FileDatabase(str(db_path))
    file_id = db.add_file(file_info, category, file_hash)
    db.log_action(file_id, "test_action", success=True)
    print(f"  File ID: {file_id}")
    print(f"  Action logged")
    
    # Step 6: Organize
    print("\n📁 Step 6: Organize")
    org_result = organize_file(str(test_file), str(organized_folder), dry_run=False)
    print(f"  Success: {org_result['success']}")
    print(f"  Destination: {org_result['destination']}")
    print(f"  Category: {org_result['category']}")
    
    # Verify
    print("\n✅ Verification")
    if org_result['success']:
        dest_file = Path(org_result['destination'])
        if dest_file.exists():
            print(f"  ✓ File moved successfully")
        else:
            print(f"  ✗ File not found at destination")
    
    # Database stats
    stats = db.get_statistics()
    print(f"\n📊 Database Statistics")
    print(f"  Total files: {stats['total_files']}")
    print(f"  By category: {stats['by_category']}")
    
    # Cleanup
    db.close()
    shutil.rmtree(test_folder)
    shutil.rmtree(organized_folder)
    print(f"\n🧹 Cleanup complete")
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)

if __name__ == "__main__":
    test_pipeline()
