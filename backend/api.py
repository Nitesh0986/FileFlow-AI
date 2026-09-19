from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from pathlib import Path
import asyncio

from backend.analyzer import analyze_file
from backend.classifier import classify_file, get_category_folder, FILE_CATEGORIES
from backend.database import FileDatabase
from backend.duplicate import find_duplicates, get_duplicate_groups
from backend.organizer import organize_file, organize_folder
from backend.renamer import rename_file, batch_rename
from backend.watcher import start_watcher

app = FastAPI(title="FileFlow-AI API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global database instance
db = FileDatabase("sample_files/incoming/fileflow.db")

# Background watcher task
watcher_task = None


# Pydantic models
class FileAnalysis(BaseModel):
    name: str
    extension: str
    size_bytes: int
    mime_type: str
    created_at: str
    modified_at: str
    path: str


class ClassificationResult(BaseModel):
    file_name: str
    category: str
    folder: str


class OrganizeRequest(BaseModel):
    source: str
    target: str
    dry_run: bool = False
    recursive: bool = True


class RenameRequest(BaseModel):
    folder: str
    pattern: Optional[str] = None
    replacement: Optional[str] = None
    sanitize: bool = False
    lowercase: bool = False
    dry_run: bool = False


class SingleRenameRequest(BaseModel):
    source_path: str
    new_name: str
    dry_run: bool = False


class WatchRequest(BaseModel):
    folder: str
    use_database: bool = True


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "FileFlow-AI API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze": "/api/analyze",
            "classify": "/api/classify",
            "organize": "/api/organize",
            "rename": "/api/rename",
            "duplicates": "/api/duplicates",
            "stats": "/api/stats",
            "files": "/api/files",
            "categories": "/api/categories"
        }
    }


@app.get("/api/categories")
async def get_categories():
    """Get all available file categories."""
    return {
        "categories": list(FILE_CATEGORIES.keys()),
        "count": len(FILE_CATEGORIES)
    }


@app.post("/api/analyze")
async def analyze_file_endpoint(file_path: str):
    """Analyze a file and return its metadata."""
    try:
        file_info = analyze_file(file_path)
        return {"success": True, "data": file_info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/classify")
async def classify_file_endpoint(file_path: str):
    """Classify a file into a category."""
    try:
        file_info = analyze_file(file_path)
        category = classify_file(file_info)
        folder = get_category_folder(category)
        
        return {
            "success": True,
            "data": {
                "file_name": file_info["name"],
                "category": category,
                "folder": folder
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/organize")
async def organize_files_endpoint(request: OrganizeRequest):
    """Organize files from source to target folder."""
    try:
        results = organize_folder(
            request.source,
            request.target,
            dry_run=request.dry_run,
            recursive=request.recursive
        )
        return {"success": True, "data": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/rename")
async def rename_files_endpoint(request: RenameRequest):
    """Batch rename files in a folder."""
    try:
        results = batch_rename(
            request.folder,
            pattern=request.pattern,
            replacement=request.replacement,
            dry_run=request.dry_run,
            sanitize=request.sanitize,
            lowercase=request.lowercase
        )
        return {"success": True, "data": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/rename/single")
async def rename_single_file_endpoint(request: SingleRenameRequest):
    """Rename a single file."""
    try:
        result = rename_file(request.source_path, request.new_name, dry_run=request.dry_run)
        
        # Log to database if successful
        if result["success"] and not request.dry_run:
            try:
                # Try to find file in database by path
                existing_file = db.get_file_by_path(request.source_path)
                if existing_file:
                    file_id = existing_file['id']
                    db.log_action(file_id, "rename", 
                                  old_path=request.source_path, 
                                  new_path=result["new_path"], 
                                  success=True)
            except Exception as e:
                # Log error but don't fail the rename operation
                print(f"Warning: Failed to log rename action: {e}")
        
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/duplicates")
async def find_duplicates_endpoint(folder_path: str):
    """Find duplicate files in a folder."""
    try:
        duplicates = find_duplicates(folder_path)
        duplicate_groups = get_duplicate_groups(duplicates)
        return {"success": True, "data": duplicate_groups}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get database statistics."""
    try:
        stats = db.get_statistics()
        return {"success": True, "data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/files")
async def get_files(category: Optional[str] = None, limit: int = 100, offset: int = 0):
    """Get files from database, optionally filtered by category."""
    try:
        if category:
            files = db.get_files_by_category(category)
        else:
            files = db.get_all_files(limit=limit, offset=offset)
        return {"success": True, "data": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/files/{file_id}")
async def get_file_by_id(file_id: int):
    """Get a specific file by ID."""
    try:
        file_data = db.get_file_by_id(file_id)
        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")
        return {"success": True, "data": file_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/files/{file_id}/actions")
async def get_file_actions(file_id: int):
    """Get all actions for a specific file."""
    try:
        actions = db.get_file_actions(file_id)
        return {"success": True, "data": actions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/watch/start")
async def start_watcher_endpoint(request: WatchRequest, background_tasks: BackgroundTasks):
    """Start the file watcher in the background."""
    try:
        # Note: This is a simplified version. In production, you'd want
        # better task management and status tracking
        background_tasks.add_task(start_watcher, request.folder, request.use_database)
        return {
            "success": True,
            "message": f"Watcher started for {request.folder}",
            "folder": request.folder
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected" if db.conn else "disconnected"
    }


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    if db:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
