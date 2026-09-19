from pathlib import Path
from typing import Dict


# File category mappings based on extensions
FILE_CATEGORIES = {
    "Documents": [
        ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx",
        ".ppt", ".pptx", ".csv", ".tex", ".epub", ".pages", ".numbers"
    ],
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp",
        ".ico", ".raw", ".heic", ".heif", ".psd", ".ai"
    ],
    "Videos": [
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v",
        ".3gp", ".mpeg", ".mpg"
    ],
    "Audio": [
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".opus",
        ".aiff", ".alac"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso",
        ".dmg", ".pkg", ".deb", ".rpm"
    ],
    "Code": [
        ".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".php",
        ".rb", ".go", ".rs", ".ts", ".jsx", ".tsx", ".vue", ".swift",
        ".kt", ".scala", ".r", ".sql", ".sh", ".bat", ".ps1", ".json",
        ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg"
    ],
    "Executables": [
        ".exe", ".msi", ".app", ".dmg", ".deb", ".rpm", ".apk", ".jar",
        ".bin", ".run"
    ],
    "Fonts": [
        ".ttf", ".otf", ".woff", ".woff2", ".eot"
    ],
    "Data": [
        ".db", ".sqlite", ".mdb", ".accdb", ".dat", ".json", ".xml",
        ".yaml", ".yml", ".parquet", ".hdf5"
    ],
    "Other": []
}


def classify_file(file_info: Dict) -> str:
    """Classify a file into a category based on its extension."""
    
    extension = file_info.get("extension", "").lower()
    
    # Check each category for a matching extension
    for category, extensions in FILE_CATEGORIES.items():
        if category == "Other":
            continue
        if extension in extensions:
            return category
    
    # If no match found, return "Other"
    return "Other"


def get_category_folder(category: str) -> str:
    """Get the folder name for a given category."""
    
    # Convert category to lowercase and replace spaces with underscores
    return category.lower().replace(" ", "_")


def print_classification(file_name: str, category: str):
    """Display the classification result."""
    
    print("\n📂 FILE CLASSIFICATION")
    print("=" * 50)
    print(f"File     : {file_name}")
    print(f"Category : {category}")
    print(f"Folder   : {get_category_folder(category)}")
    print("=" * 50)


if __name__ == "__main__":
    # Test the classifier
    test_files = [
        {"name": "document.pdf", "extension": ".pdf"},
        {"name": "image.jpg", "extension": ".jpg"},
        {"name": "video.mp4", "extension": ".mp4"},
        {"name": "script.py", "extension": ".py"},
        {"name": "archive.zip", "extension": ".zip"},
        {"name": "unknown.xyz", "extension": ".xyz"},
    ]
    
    print("🧪 CLASSIFIER TEST")
    print("=" * 50)
    
    for file_info in test_files:
        category = classify_file(file_info)
        print(f"{file_info['name']:20} -> {category}")
    
    print("=" * 50)
