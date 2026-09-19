# FileFlow-AI
AI-powered privacy-first desktop assistant that intelligentlyclassifies, renames, organizes, and manages local files in real time.
🚀 FileFlow AI

An AI-powered, privacy-first local file organization assistant

FileFlow AI is a desktop productivity application designed to
automatically understand, classify, rename, and organize files on a
user's computer.

🏆 Hackathon

HackDevengers 2.0 --- 2026

FileFlow AI is being developed as an original open-innovation project
for the hackathon.

💡 Problem

Users accumulate downloaded documents, resumes, certificates, invoices,
notes, images, archives, and duplicate files. Generic filenames and
manual folder management make local storage difficult to maintain.

💡 Solution

FileFlow AI monitors selected local folders, analyzes incoming files,
classifies them, suggests meaningful names and categories, creates
folders when needed, moves files, detects duplicates, and records
actions so users can review or undo supported operations.

New File
   ↓
File Watcher
   ↓
Metadata / Content Analysis
   ↓
AI Classification
   ↓
Smart Filename
   ↓
Safety Check
   ↓
Move / Rename
   ↓
Activity Log
   ↓
Dashboard / Undo

✨ Key Features

📡 Real-time file monitoring

🧠 Content-aware AI classification

✏️ Smart file renaming

📁 Automatic folder creation

🔍 Duplicate detection

↩️ Activity history and undo

📊 Dashboard for organized files and recent actions

🏗️ Planned Architecture

Local File System
       ↓
File Watcher (Watchdog)
       ↓
File Analyzer
       ↓
AI Classification
       ↓
Safety / Validation
       ↓
Organization Engine
       ↓
SQLite Activity Log
       ↓
React Dashboard

🛠️ Technology Stack

Backend / Desktop Engine

Python

Watchdog

pathlib / OS APIs

shutil

hashlib

PyMuPDF

SQLite

AI

The AI layer will be used for semantic classification, document
understanding, and smart filename generation. The exact model/provider
will be selected during implementation based on reliability and
hackathon constraints.

Frontend

React

Vite

CSS / Tailwind CSS

API

FastAPI

🔐 Privacy & Safety

FileFlow AI follows a local-first design:

No automatic file deletion in the MVP.

User-selected folders only.

Operations are logged.

Supported operations can be undone.

Local processing is preferred where practical.

External AI services receive only the minimum information required
when they are used.

System-critical directories should not be monitored.

📂 Planned Structure

FileFlow-AI/
├── backend/
│   ├── main.py
│   ├── watcher.py
│   ├── organizer.py
│   ├── classifier.py
│   ├── renamer.py
│   ├── duplicate.py
│   └── database.py
├── frontend/
├── sample_files/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt

🚀 MVP Roadmap

Phase 1 --- Core Automation

Project setup

Folder monitoring

New-file detection

File categorization

Automatic folder creation

Safe file movement

Phase 2 --- AI

PDF text extraction

AI classification

Smart filename generation

Confidence / reasoning information

Phase 3 --- Safety

Duplicate detection

Activity history

Undo

Filename conflict handling

Error handling

Phase 4 --- Dashboard

React dashboard

Statistics

Recent activity

Action details

Manual review controls

🎯 Example

Before

Downloads/
├── download123.pdf
├── bill9382.pdf
├── resume_final2.pdf
├── IMG_8273.jpg
└── notes.zip

After

FileFlow/
├── Career/
│   └── Nitesh_Resume_2026.pdf
├── Finance/
│   └── Electricity_Bill_Sep_2026.pdf
├── Images/
│   └── IMG_8273.jpg
└── Archives/
    └── Notes.zip

🧪 Demo Scenario

Select a Downloads folder.

Add several sample files.

FileFlow detects the new files.

Files are analyzed and classified.

Meaningful names and destinations are suggested.

Files are organized.

The dashboard shows the activity.

A supported operation is reversed using Undo.

🌱 Future Scope

Semantic local file search

OCR for scanned documents

Natural-language organization rules

Version tracking

Similar-file detection

On-device AI models

Document expiry detection

Personal document profiles

Natural-language commands

⚠️ Safety

File-system automation must be reversible and predictable. The MVP will
avoid automatic deletion, validate paths, handle filename conflicts, log
operations, and restrict monitoring to user-selected directories.

👨‍💻 Author

Nitesh Kumar Barnwal
B.Tech --- Computer Science & Engineering
Narula Institute of Technology

📌 Project Status

🚧 Active development for HackDevengers 2.0

The repository will be updated as features are implemented and tested
during the hackathon.

📄 License

License details will be added according to the final project
requirements.