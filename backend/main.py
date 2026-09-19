#!/usr/bin/env python3
"""
FileFlow-AI Main Entry Point
Integrates all modules for file organization and management.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from analyzer import analyze_file, print_file_info
from classifier import classify_file, get_category_folder, print_classification
from database import FileDatabase
from duplicate import calculate_file_hash, find_duplicates, get_duplicate_groups, print_duplicates
from organizer import organize_file, organize_folder, print_organization_results, create_category_structure
from renamer import rename_file, batch_rename, print_rename_results, sanitize_filename


def cmd_analyze(args):
    """Analyze a file and display its information."""
    
    try:
        file_info = analyze_file(args.file)
        print_file_info(file_info)
        
        # Also classify the file
        category = classify_file(file_info)
        print_classification(file_info["name"], category)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def cmd_classify(args):
    """Classify a file into a category."""
    
    try:
        file_info = analyze_file(args.file)
        category = classify_file(file_info)
        folder = get_category_folder(category)
        
        print_classification(file_info["name"], category)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def cmd_organize(args):
    """Organize files into category folders."""
    
    try:
        results = organize_folder(
            args.source,
            args.target,
            dry_run=args.dry_run,
            recursive=args.recursive
        )
        print_organization_results(results)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def cmd_rename(args):
    """Rename files with various options."""
    
    try:
        results = batch_rename(
            args.folder,
            pattern=args.pattern,
            replacement=args.replacement,
            dry_run=args.dry_run,
            sanitize=args.sanitize,
            lowercase=args.lowercase
        )
        print_rename_results(results)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def cmd_duplicate(args):
    """Find duplicate files."""
    
    try:
        duplicates = find_duplicates(args.folder, args.algorithm)
        duplicate_groups = get_duplicate_groups(duplicates)
        print_duplicates(duplicate_groups)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def cmd_watch(args):
    """Watch a folder for new files and process them."""
    
    try:
        from watcher import start_watcher
        start_watcher(args.folder)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def cmd_stats(args):
    """Display database statistics."""
    
    try:
        db_path = args.database if args.database else "fileflow.db"
        
        with FileDatabase(db_path) as db:
            stats = db.get_statistics()
            
            print("\n📊 FILEFLOW STATISTICS")
            print("=" * 60)
            print(f"Total files: {stats['total_files']}")
            print(f"Total duplicates: {stats['total_duplicates']}")
            print(f"Total size: {stats['total_size_bytes']:,} bytes ({stats['total_size_bytes'] / (1024*1024):.2f} MB)")
            
            if stats['by_category']:
                print("\n📂 Files by category:")
                for category, count in stats['by_category'].items():
                    print(f"   {category}: {count}")
            
            print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def cmd_init(args):
    """Initialize FileFlow-AI structure."""
    
    try:
        base_path = Path(args.path)
        
        # Create category structure
        create_category_structure(base_path)
        
        # Initialize database
        db_path = base_path / "fileflow.db"
        with FileDatabase(str(db_path)) as db:
            print(f"✓ Database created: {db_path}")
        
        print("\n✅ FileFlow-AI initialized successfully!")
        print(f"Base path: {base_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point for FileFlow-AI CLI."""
    
    parser = argparse.ArgumentParser(
        description="FileFlow-AI - Intelligent File Organization System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a file
  python main.py analyze myfile.pdf
  
  # Classify a file
  python main.py classify myfile.pdf
  
  # Organize a folder
  python main.py organize ./downloads ./organized
  
  # Find duplicates
  python main.py duplicate ./downloads
  
  # Watch a folder
  python main.py watch ./downloads
  
  # Show statistics
  python main.py stats
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a file")
    analyze_parser.add_argument("file", help="File path to analyze")
    analyze_parser.set_defaults(func=cmd_analyze)
    
    # Classify command
    classify_parser = subparsers.add_parser("classify", help="Classify a file")
    classify_parser.add_argument("file", help="File path to classify")
    classify_parser.set_defaults(func=cmd_classify)
    
    # Organize command
    organize_parser = subparsers.add_parser("organize", help="Organize files into categories")
    organize_parser.add_argument("source", help="Source folder")
    organize_parser.add_argument("target", help="Target folder")
    organize_parser.add_argument("--dry-run", action="store_true", help="Preview without moving")
    organize_parser.add_argument("--recursive", action="store_true", default=True, help="Process subdirectories")
    organize_parser.set_defaults(func=cmd_organize)
    
    # Rename command
    rename_parser = subparsers.add_parser("rename", help="Batch rename files")
    rename_parser.add_argument("folder", help="Folder containing files to rename")
    rename_parser.add_argument("--pattern", help="Pattern to replace")
    rename_parser.add_argument("--replacement", help="Replacement string")
    rename_parser.add_argument("--sanitize", action="store_true", help="Sanitize filenames")
    rename_parser.add_argument("--lowercase", action="store_true", help="Convert to lowercase")
    rename_parser.add_argument("--dry-run", action="store_true", help="Preview without renaming")
    rename_parser.set_defaults(func=cmd_rename)
    
    # Duplicate command
    duplicate_parser = subparsers.add_parser("duplicate", help="Find duplicate files")
    duplicate_parser.add_argument("folder", help="Folder to scan")
    duplicate_parser.add_argument("--algorithm", default="sha256", 
                                 choices=["md5", "sha1", "sha256"],
                                 help="Hash algorithm to use")
    duplicate_parser.set_defaults(func=cmd_duplicate)
    
    # Watch command
    watch_parser = subparsers.add_parser("watch", help="Watch folder for new files")
    watch_parser.add_argument("folder", help="Folder to watch")
    watch_parser.set_defaults(func=cmd_watch)
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show database statistics")
    stats_parser.add_argument("--database", help="Database file path")
    stats_parser.set_defaults(func=cmd_stats)
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize FileFlow-AI structure")
    init_parser.add_argument("path", nargs="?", default=".", help="Base path for initialization")
    init_parser.set_defaults(func=cmd_init)
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command provided, show help
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    args.func(args)


if __name__ == "__main__":
    main()
