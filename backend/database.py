import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json


class FileDatabase:
    """SQLite database for storing file metadata and tracking."""
    
    def __init__(self, db_path: str = "fileflow.db"):
        """Initialize the database connection."""
        
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish database connection."""
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def _create_tables(self):
        """Create necessary tables if they don't exist."""
        
        # Files table - stores file metadata
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                extension TEXT,
                size_bytes INTEGER,
                mime_type TEXT,
                category TEXT,
                created_at TEXT,
                modified_at TEXT,
                file_hash TEXT,
                first_seen TEXT,
                last_seen TEXT,
                is_duplicate BOOLEAN DEFAULT 0,
                original_file_id INTEGER,
                FOREIGN KEY (original_file_id) REFERENCES files(id)
            )
        """)
        
        # Actions table - tracks file operations
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER NOT NULL,
                action_type TEXT NOT NULL,
                old_path TEXT,
                new_path TEXT,
                timestamp TEXT NOT NULL,
                success BOOLEAN DEFAULT 1,
                error_message TEXT,
                FOREIGN KEY (file_id) REFERENCES files(id)
            )
        """)
        
        # Statistics table - stores aggregate stats
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stat_name TEXT UNIQUE NOT NULL,
                stat_value TEXT,
                updated_at TEXT
            )
        """)
        
        self.conn.commit()
    
    def add_file(self, file_info: Dict, category: str = None, file_hash: str = None) -> int:
        """Add a new file record to the database."""
        
        now = datetime.now().isoformat()
        
        try:
            self.cursor.execute("""
                INSERT INTO files (
                    file_path, name, extension, size_bytes, mime_type,
                    category, created_at, modified_at, file_hash,
                    first_seen, last_seen
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                file_info["path"],
                file_info["name"],
                file_info["extension"],
                file_info["size_bytes"],
                file_info["mime_type"],
                category,
                file_info["created_at"],
                file_info["modified_at"],
                file_hash,
                now,
                now
            ))
            
            self.conn.commit()
            return self.cursor.lastrowid
            
        except sqlite3.IntegrityError:
            # File already exists, update last_seen
            self.cursor.execute("""
                UPDATE files 
                SET last_seen = ?, category = ?, file_hash = ?
                WHERE file_path = ?
            """, (now, category, file_hash, file_info["path"]))
            
            self.conn.commit()
            
            # Get the file ID
            self.cursor.execute(
                "SELECT id FROM files WHERE file_path = ?",
                (file_info["path"],)
            )
            result = self.cursor.fetchone()
            return result[0] if result else None
    
    def get_file_by_path(self, file_path: str) -> Optional[Dict]:
        """Retrieve file information by path."""
        
        self.cursor.execute("""
            SELECT * FROM files WHERE file_path = ?
        """, (file_path,))
        
        row = self.cursor.fetchone()
        
        if row:
            columns = [desc[0] for desc in self.cursor.description]
            return dict(zip(columns, row))
        
        return None
    
    def get_file_by_id(self, file_id: int) -> Optional[Dict]:
        """Retrieve file information by ID."""
        
        self.cursor.execute("""
            SELECT * FROM files WHERE id = ?
        """, (file_id,))
        
        row = self.cursor.fetchone()
        
        if row:
            columns = [desc[0] for desc in self.cursor.description]
            return dict(zip(columns, row))
        
        return None
    
    def get_files_by_category(self, category: str) -> List[Dict]:
        """Retrieve all files in a specific category."""
        
        self.cursor.execute("""
            SELECT * FROM files WHERE category = ?
        """, (category,))
        
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        
        return [dict(zip(columns, row)) for row in rows]
    
    def get_all_files(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Retrieve all files with pagination."""
        
        self.cursor.execute("""
            SELECT * FROM files ORDER BY first_seen DESC LIMIT ? OFFSET ?
        """, (limit, offset))
        
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        
        return [dict(zip(columns, row)) for row in rows]
    
    def get_duplicates(self) -> List[Dict]:
        """Retrieve all duplicate files."""
        
        self.cursor.execute("""
            SELECT * FROM files WHERE is_duplicate = 1
        """)
        
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        
        return [dict(zip(columns, row)) for row in rows]
    
    def mark_duplicate(self, file_id: int, original_file_id: int):
        """Mark a file as a duplicate."""
        
        self.cursor.execute("""
            UPDATE files 
            SET is_duplicate = 1, original_file_id = ?
            WHERE id = ?
        """, (original_file_id, file_id))
        
        self.conn.commit()
    
    def log_action(self, file_id: int, action_type: str, 
                   old_path: str = None, new_path: str = None,
                   success: bool = True, error_message: str = None):
        """Log a file action to the database."""
        
        timestamp = datetime.now().isoformat()
        
        self.cursor.execute("""
            INSERT INTO actions (
                file_id, action_type, old_path, new_path,
                timestamp, success, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (file_id, action_type, old_path, new_path, 
              timestamp, success, error_message))
        
        self.conn.commit()
    
    def get_file_actions(self, file_id: int) -> List[Dict]:
        """Get all actions performed on a file."""
        
        self.cursor.execute("""
            SELECT * FROM actions WHERE file_id = ? ORDER BY timestamp DESC
        """, (file_id,))
        
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        
        return [dict(zip(columns, row)) for row in rows]
    
    def get_statistics(self) -> Dict:
        """Get database statistics."""
        
        stats = {}
        
        # Total files
        self.cursor.execute("SELECT COUNT(*) FROM files")
        stats["total_files"] = self.cursor.fetchone()[0]
        
        # Files by category
        self.cursor.execute("""
            SELECT category, COUNT(*) FROM files 
            WHERE category IS NOT NULL 
            GROUP BY category
        """)
        stats["by_category"] = dict(self.cursor.fetchall())
        
        # Total duplicates
        self.cursor.execute("SELECT COUNT(*) FROM files WHERE is_duplicate = 1")
        stats["total_duplicates"] = self.cursor.fetchone()[0]
        
        # Total size
        self.cursor.execute("SELECT SUM(size_bytes) FROM files")
        result = self.cursor.fetchone()[0]
        stats["total_size_bytes"] = result if result else 0
        
        return stats
    
    def update_file_path(self, file_id: int, new_path: str):
        """Update file path after move/rename."""
        
        self.cursor.execute("""
            UPDATE files SET file_path = ? WHERE id = ?
        """, (new_path, file_id))
        
        self.conn.commit()
    
    def delete_file(self, file_id: int):
        """Delete a file record from the database."""
        
        self.cursor.execute("DELETE FROM actions WHERE file_id = ?", (file_id,))
        self.cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))
        self.conn.commit()
    
    def close(self):
        """Close database connection."""
        
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


if __name__ == "__main__":
    # Test the database
    print("🧪 DATABASE TEST")
    print("=" * 50)
    
    with FileDatabase("test_fileflow.db") as db:
        # Test adding a file
        test_file = {
            "name": "test.txt",
            "extension": ".txt",
            "size_bytes": 1024,
            "mime_type": "text/plain",
            "created_at": "2024-01-01T00:00:00",
            "modified_at": "2024-01-01T00:00:00",
            "path": "/tmp/test.txt"
        }
        
        file_id = db.add_file(test_file, category="Documents")
        print(f"✓ Added file with ID: {file_id}")
        
        # Test retrieving file
        retrieved = db.get_file_by_id(file_id)
        print(f"✓ Retrieved file: {retrieved['name']}")
        
        # Test statistics
        stats = db.get_statistics()
        print(f"✓ Statistics: {stats}")
        
        # Test logging action
        db.log_action(file_id, "test_action", success=True)
        print("✓ Logged action")
        
    print("=" * 50)
    print("Database test completed!")
