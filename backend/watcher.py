from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from backend.analyzer import analyze_file, print_file_info
from backend.classifier import classify_file, print_classification
from backend.database import FileDatabase
from backend.duplicate import calculate_file_hash
from backend.organizer import organize_file
from backend.renamer import sanitize_filename, replace_spaces

class FileFlowHandler(FileSystemEventHandler):
    """Handles file-system events detected by Watchdog."""
    
    def __init__(self, db: FileDatabase = None, target_folder: str = None):
        """Initialize handler with optional database and target folder."""
        self.db = db
        self.target_folder = target_folder
        self.processed_files = set()  # Track processed files to avoid duplicates

    def on_created(self, event):
        """Called whenever a new file or folder is created."""

        # Ignore folders
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Skip if already processed (avoid duplicate events)
        if str(file_path) in self.processed_files:
            return

        self.processed_files.add(str(file_path))

        # Ignore database files and temporary files
        if file_path.suffix in ['.db', '.db-journal', '.tmp', '.temp']:
            return

        print("\n" + "=" * 60)
        print(" NEW FILE DETECTED")
        print("=" * 60)

        print(f"Name      : {file_path.name}")
        print(f"Extension : {file_path.suffix}")
        print(f"Path      : {file_path}")

        # Complete processing pipeline
        try:
            # Step 1: Analyze
            file_info = analyze_file(str(file_path))
            print_file_info(file_info)
            
            # Step 2: Classify
            category = classify_file(file_info)
            print_classification(file_info["name"], category)
            
            # Step 3: Generate smart filename
            original_name = file_info["name"]
            smart_name = sanitize_filename(original_name)
            smart_name = replace_spaces(smart_name, "_")
            print(f"Smart Name: {smart_name}")
            
            # Step 4: Calculate hash for duplicate detection
            file_hash = calculate_file_hash(str(file_path))
            print(f"Hash      : {file_hash[:16]}...")
            
            # Step 5: Check for duplicates in database
            is_duplicate = False
            if self.db:
                # Check all files in database for duplicate hash
                all_files = self.db.get_all_files(limit=1000)
                for existing_file in all_files:
                    if existing_file.get('file_hash') == file_hash:
                        is_duplicate = True
                        print(f" Duplicate detected (same hash as {existing_file['name']})")
                        break
            
            # Step 6: Organize file if target folder specified
            if self.target_folder and not is_duplicate:
                print(f"\n Organizing to: {self.target_folder}")
                org_result = organize_file(str(file_path), self.target_folder, dry_run=False)
                
                if org_result["success"]:
                    print(f" Moved to: {org_result['destination']}")
                    print(f"  Category: {org_result['category']}")
                    
                    # Update file path in database
                    if self.db:
                        file_id = self.db.add_file(file_info, category, file_hash)
                        self.db.update_file_path(file_id, org_result['destination'])
                        self.db.log_action(file_id, "file_organized", 
                                          old_path=str(file_path), 
                                          new_path=org_result['destination'], 
                                          success=True)
                        print(f"Database  : Updated (ID: {file_id})")
                else:
                    print(f" Organization failed: {org_result['error']}")
            else:
                # Just store in database without moving
                if self.db:
                    file_id = self.db.add_file(file_info, category, file_hash)
                    self.db.log_action(file_id, "file_created", success=True)
                    print(f"Database  : Stored (ID: {file_id})")

        except Exception as error:
            print("\n FILE PROCESSING FAILED")
            print(f"Reason: {error}")
            import traceback
            traceback.print_exc()

        print("=" * 60)


def start_watcher(folder_path: str, use_database: bool = True, target_folder: str = None):
    """Start monitoring the selected folder."""

    folder = Path(folder_path)

    # Check whether folder exists
    if not folder.exists():
        raise FileNotFoundError(
            f"Folder does not exist: {folder}"
        )

    # Check whether path is actually a directory
    if not folder.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {folder}"
        )

    # Initialize database if enabled
    db = None
    if use_database:
        db_path = folder / "fileflow.db"
        db = FileDatabase(str(db_path))

    # Create event handler with database and target folder
    event_handler = FileFlowHandler(db, target_folder)

    # Create Watchdog observer
    observer = Observer()

    # Monitor folder recursively
    observer.schedule(
        event_handler,
        str(folder),
        recursive=True
    )

    # Start observer
    observer.start()

    print("\n" + "=" * 60)
    print(" FILEFLOW AI WATCHER")
    print("=" * 60)
    print(f" Monitoring: {folder}")
    print(" Status: ACTIVE")
    print(" Analyzer: ENABLED")
    print(" Classifier: ENABLED")
    print(" Renamer: ENABLED")
    print(" Hash Calculator: ENABLED")
    print(" Organizer: ENABLED" if target_folder else " Organizer: DISABLED")
    if db:
        print(" Database: ENABLED")
    else:
        print(" Database: DISABLED")
    if target_folder:
        print(f" Target: {target_folder}")
    print("Waiting for new files...")
    print("Press CTRL+C to stop.")
    print("=" * 60)

    try:
        while True:
            input()

    except KeyboardInterrupt:
        print("\n Stopping FileFlow AI...")

        observer.stop()

        # Close database connection
        if db:
            db.close()

    observer.join()


if __name__ == "__main__":

    base_folder = Path(__file__).resolve().parent.parent / "sample_files"
    incoming_folder = base_folder / "incoming"
    organized_folder = base_folder / "organized"

    start_watcher(
        str(incoming_folder),
        use_database=True,
        target_folder=str(organized_folder)
    )