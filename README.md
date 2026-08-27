# 🕵️ Disk Space Detective

> **Find out where your storage went.**

Disk Space Detective is a Python-based desktop application that investigates disk usage and helps users understand what is consuming their computer's storage.

Instead of simply displaying disk usage such as:

```text
Videos       20 GB
Pictures     10 GB
Documents    5 GB
```

Disk Space Detective investigates **why the storage is being used** and identifies potentially unnecessary or unusual storage consumers.

For example:

```text
🔎 Storage Investigation

Your disk usage increased by 8.4 GB.

Possible causes:

Chrome Cache             +2.1 GB
Downloads                +1.8 GB
node_modules             +1.7 GB
Python environments      +1.2 GB
Temporary files          +0.9 GB
Other                    +0.7 GB
```

It can also identify findings such as:

```text
⚠️ Detective Finding

14 old node_modules directories
Total size: 6.2 GB

These directories may be removable because
their dependencies can usually be recreated.
```

---

## 🎯 Project Goals

The main goals of Disk Space Detective are:

* Analyze available disk space.
* Identify large folders and files.
* Detect common storage-consuming developer folders.
* Categorize disk usage.
* Detect old or potentially unnecessary files/folders.
* Compare current and previous scans.
* Explain possible reasons for storage growth.
* Provide safe cleanup recommendations.
* Present the results through a simple desktop interface.

The application will **not automatically delete files**. It will provide information and recommendations while leaving the final cleanup decision to the user.

---

# 🛠️ Technology Stack

### Programming Language

* Python

### Desktop GUI

* PySide6

### System / File Management

* `pathlib`
* `os`
* `shutil`
* `psutil`

### Database

* SQLite

### Testing

* pytest

### Version Control

* Git
* GitHub

### Packaging

* PyInstaller

---

# 📁 Planned Project Structure

```text
disk-space-detective/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── disk_scanner.py
│   ├── folder_scanner.py
│   ├── file_scanner.py
│   ├── categories.py
│   ├── analyzer.py
│   ├── detector.py
│   └── recommendations.py
│
├── database/
│   ├── __init__.py
│   ├── database.py
│   └── models.py
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── dashboard.py
│   ├── scan_view.py
│   ├── results_view.py
│   ├── findings_view.py
│   └── history_view.py
│
├── utils/
│   ├── __init__.py
│   ├── formatters.py
│   └── constants.py
│
├── tests/
│   ├── test_scanner.py
│   ├── test_analyzer.py
│   └── test_categories.py
│
└── data/
    └── scans.db
```

---

# 🔄 Planned Architecture

The application will follow this general flow:

```text
                User
                 │
                 ▼
          Select Disk / Drive
                 │
                 ▼
          ┌──────────────┐
          │ Disk Scanner │
          └──────┬───────┘
                 │
                 ▼
         File & Folder Data
                 │
                 ▼
          ┌──────────────┐
          │   Analyzer   │
          └──────┬───────┘
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
   Categories  Findings  Changes
       │         │         │
       └─────────┼─────────┘
                 ▼
          Recommendations
                 │
                 ▼
          SQLite / History
                 │
                 ▼
          PySide6 Dashboard
```

---

# ⭐ Planned Features

## Phase 1 — Basic Scanner

* [ ] Detect available drives.
* [ ] Display total disk capacity.
* [ ] Display used space.
* [ ] Display free space.
* [ ] Scan folders.
* [ ] Calculate folder sizes.
* [ ] Handle permission errors.

## Phase 2 — Storage Investigation

* [ ] Detect large files.
* [ ] Detect large folders.
* [ ] Identify `node_modules`.
* [ ] Identify Python virtual environments.
* [ ] Identify `__pycache__`.
* [ ] Identify build folders.
* [ ] Identify temporary files.
* [ ] Categorize storage usage.

## Phase 3 — Detective Findings

* [ ] Detect old folders.
* [ ] Detect old files.
* [ ] Identify potentially unnecessary development folders.
* [ ] Generate storage findings.
* [ ] Generate cleanup recommendations.

## Phase 4 — Scan History

* [ ] Store scan results.
* [ ] Display previous scans.
* [ ] Compare two scans.
* [ ] Detect storage growth.
* [ ] Identify categories responsible for growth.

Example:

```text
Previous scan: 421.0 GB
Current scan: 429.4 GB

Storage increased: +8.4 GB

Main contributors:

node_modules       +2.1 GB
Downloads          +1.8 GB
Python environments +1.2 GB
```

## Phase 5 — Desktop Application

* [ ] Create PySide6 main window.
* [ ] Create dashboard.
* [ ] Create scan screen.
* [ ] Create results screen.
* [ ] Create findings screen.
* [ ] Create scan history screen.
* [ ] Add charts and visualizations.
* [ ] Add progress indicator.
* [ ] Improve UI/UX.

## Phase 6 — Advanced Features

Possible future features:

* [ ] Duplicate file detection.
* [ ] File hashing.
* [ ] More advanced cache detection.
* [ ] Export reports.
* [ ] Scheduled scans.
* [ ] AI-powered explanations.
* [ ] Safe cleanup assistance.
* [ ] Windows `.exe` packaging.

---

# 👩‍💻 Task Assignment

The project has two main development areas.

## 👩 Developer 1 — Core Scanner & Analysis

**Main responsibility:** Python backend / investigation engine

### Scanner

* [ ] `disk_scanner.py`
* [ ] `folder_scanner.py`
* [ ] `file_scanner.py`

### Analysis

* [ ] `categories.py`
* [ ] `analyzer.py`
* [ ] `detector.py`
* [ ] `recommendations.py`

### Responsibilities

* Drive detection
* Disk usage calculation
* Recursive folder scanning
* File size calculation
* Large file detection
* Developer folder detection
* Storage categorization
* Old file/folder detection
* Investigation logic
* Cleanup recommendations

---

## 👩‍💻 Developer 2 — Desktop UI & Database

**Main responsibility:** Application interface and data storage

### UI

* [ ] `main_window.py`
* [ ] `dashboard.py`
* [ ] `scan_view.py`
* [ ] `results_view.py`
* [ ] `findings_view.py`
* [ ] `history_view.py`

### Database

* [ ] `database.py`
* [ ] `models.py`

### Responsibilities

* PySide6 application
* Dashboard design
* Scan interface
* Results interface
* Findings interface
* Charts
* Progress indicators
* Scan history
* SQLite storage
* Connecting scanner results to UI

---

# 🤝 Shared Responsibilities

Both developers will work together on:

* [ ] Project planning
* [ ] GitHub repository management
* [ ] Code reviews
* [ ] Testing
* [ ] Bug fixing
* [ ] Integration
* [ ] Documentation
* [ ] README
* [ ] Final UI improvements
* [ ] Project presentation
* [ ] Final testing
* [ ] Packaging the application

---

# 🌿 Git Workflow

The `main` branch should contain stable code.

Developers should create feature branches before working.

Example:

```text
main
│
├── feature/disk-scanner
├── feature/folder-scanner
├── feature/file-detector
├── feature/analyzer
├── feature/dashboard
├── feature/database
└── feature/history
```

### Basic workflow

```text
Create feature branch
        ↓
Implement feature
        ↓
Test
        ↓
Commit
        ↓
Push to GitHub
        ↓
Create Pull Request
        ↓
Review
        ↓
Merge into main
```

Avoid directly making changes to `main` unless both developers agree.

---

# 📌 Important Development Rule

The scanner and UI should be kept separate.

The scanner should produce structured data rather than directly controlling the GUI.

For example:

```python
{
    "path": "C:/Projects/example/node_modules",
    "size": 1240000000,
    "category": "node_modules",
    "last_modified": "2026-08-20"
}
```

The UI can then display this information without needing to know how the size was calculated.

This separation will make the application easier to test, maintain and extend.

---

# 🚧 Current Status

**Project stage:** Planning / Initial Development

### Current priority

1. Set up repository.
2. Create project structure.
3. Set up Python virtual environment.
4. Install initial dependencies.
5. Implement basic disk scanner.
6. Implement folder scanning.
7. Build the first working scan.
8. Begin PySide6 interface.
9. Connect scanner to interface.

---

# 💡 Future Vision

The final application should allow a user to open Disk Space Detective and see:

```text
🕵️ DISK SPACE DETECTIVE

Your C: drive is 85% full.

Used: 438 GB
Free: 74 GB

────────────────────────────────

🔎 WHERE DID YOUR SPACE GO?

Development          18.4 GB
Downloads            12.7 GB
Browser Cache         6.3 GB
Temporary Files       4.8 GB

────────────────────────────────

🚨 DETECTIVE FINDINGS

14 old node_modules
6.2 GB

8 old Python environments
3.4 GB

37 large files
12.8 GB

────────────────────────────────

📈 SINCE LAST SCAN

Storage increased by 8.4 GB

Most likely cause:
Development dependencies
```

**The goal is not just to show disk usage, but to investigate and explain it.**

---

## 👥 Contributors

* **Developer 1:** Core Scanner & Analysis
* **Developer 2:** Desktop UI & Database

*Roles can be adjusted as the project develops.*

