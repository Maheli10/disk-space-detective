from pathlib import Path
from datetime import datetime, timedelta

from core.folderScanner import get_folder_size
from core.categories import get_file_category


# Directories that should be ignored when analyzing
# file categories and old files.
IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__"
}


def should_ignore(path):
    """Check whether a path is inside an ignored directory."""

    return any(
        part in IGNORED_DIRECTORIES
        for part in path.parts
    )


def analyze_folders(folder_path, limit=10):
    """
    Find the largest folders inside a directory.
    """

    folder = Path(folder_path)

    folder_sizes = []

    try:

        for item in folder.iterdir():

            if item.is_dir():

                try:

                    size = get_folder_size(item)

                    folder_sizes.append({
                        "name": item.name,
                        "path": item,
                        "size": size
                    })

                except (PermissionError, OSError):
                    continue

    except (PermissionError, OSError):
        return []

    # Sort from largest to smallest
    folder_sizes.sort(
        key=lambda folder: folder["size"],
        reverse=True
    )

    return folder_sizes[:limit]


def analyze_file_categories(folder_path):
    """
    Calculate how much space different file categories use.

    Generated and dependency directories are ignored
    to make the category results more meaningful.
    """

    folder = Path(folder_path)

    category_sizes = {}

    for item in folder.rglob("*"):

        try:

            if item.is_file():

                # Ignore generated and dependency folders
                if should_ignore(item):
                    continue

                size = item.stat().st_size

                category = get_file_category(item)

                if category not in category_sizes:
                    category_sizes[category] = 0

                category_sizes[category] += size

        except (PermissionError, OSError):
            continue

    # Convert dictionary into a sorted list
    results = []

    for category, size in category_sizes.items():

        results.append({
            "category": category,
            "size": size
        })

    # Sort from largest to smallest
    results.sort(
        key=lambda item: item["size"],
        reverse=True
    )

    return results


def find_old_files(folder_path, days=180, limit=10):
    """
    Find files that have not been modified for a long time.

    Default: files older than 180 days.

    Generated and dependency directories are ignored
    because their files are normally not useful
    as old-file findings.
    """

    folder = Path(folder_path)

    cutoff_date = datetime.now() - timedelta(days=days)

    old_files = []

    for item in folder.rglob("*"):

        try:

            if item.is_file():

                # Ignore generated and dependency folders
                if should_ignore(item):
                    continue

                modified_time = datetime.fromtimestamp(
                    item.stat().st_mtime
                )

                if modified_time < cutoff_date:

                    old_files.append({
                        "name": item.name,
                        "path": item,
                        "size": item.stat().st_size,
                        "modified": modified_time
                    })

        except (PermissionError, OSError, ValueError):
            continue

    # Biggest old files first
    old_files.sort(
        key=lambda file: file["size"],
        reverse=True
    )

    return old_files[:limit]


def calculate_total_size(items):
    """
    Calculate the total size of a list of findings.
    """

    total = 0

    for item in items:

        total += item["size"]

    return total


