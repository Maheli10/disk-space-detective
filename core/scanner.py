import os
import heapq
from pathlib import Path
from datetime import datetime, timedelta

from core.categories import get_file_category


IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__"
}

IGNORED_DIRECTORIES_LOWER = {
    directory.lower()
    for directory in IGNORED_DIRECTORIES
}

SPECIAL_FOLDERS = {
    "node_modules": "Node Modules",
    "venv": "Python Virtual Environment",
    ".venv": "Python Virtual Environment",
    "__pycache__": "Python Cache"
}

TEMP_FOLDER_NAMES = {
    "temp",
    "tmp",
    "cache"
}

MIN_LARGE_FILE_SIZE = 100 * 1024 * 1024
MIN_CACHE_SIZE = 10 * 1024 * 1024
MIN_DUPLICATE_SIZE = 10 * 1024 * 1024

MAX_LARGE_FILES = 10
MAX_CACHE_FOLDERS = 10
MAX_SPECIAL_FOLDERS = 20
MAX_OLD_FILES = 10


def scan_filesystem(folder_path):
    """
    Perform a single filesystem scan.

    Collects:
    - total storage size
    - file information
    - folder sizes
    - largest files
    - old files
    - file categories
    - special folders
    - cache/temp folders
    - duplicate candidates
    - top-level folders
    """

    root = Path(folder_path)

    if not root.exists():
        raise ValueError(f"Folder does not exist: {root}")

    if not root.is_dir():
        raise ValueError(f"Path is not a directory: {root}")

    files = []
    folder_sizes = {}
    category_sizes = {}

    special_folders = []
    cache_folders = []

    duplicate_candidates = {}

    large_files_heap = []
    old_files_heap = []

    cutoff_timestamp = (
        datetime.now() - timedelta(days=180)
    ).timestamp()

    def add_large_file(file_data):
        """Keep only the largest files."""

        item = (
            file_data["size"],
            file_data
        )

        if len(large_files_heap) < MAX_LARGE_FILES:
            heapq.heappush(
                large_files_heap,
                item
            )

        elif file_data["size"] > large_files_heap[0][0]:
            heapq.heapreplace(
                large_files_heap,
                item
            )

    def add_old_file(file_data):
        """Keep only the largest old files."""

        item = (
            file_data["size"],
            file_data
        )

        if len(old_files_heap) < MAX_OLD_FILES:
            heapq.heappush(
                old_files_heap,
                item
            )

        elif file_data["size"] > old_files_heap[0][0]:
            heapq.heapreplace(
                old_files_heap,
                item
            )

    def scan_directory(directory, ignored=False):
        """Recursively scan a directory."""

        total_size = 0

        try:
            with os.scandir(directory) as entries:

                for entry in entries:

                    try:
                        if entry.is_symlink():
                            continue

                        if entry.is_dir(
                            follow_symlinks=False
                        ):

                            folder_name = entry.name.lower()

                            child_ignored = (
                                ignored
                                or folder_name
                                in IGNORED_DIRECTORIES_LOWER
                            )

                            child_size = scan_directory(
                                entry.path,
                                child_ignored
                            )

                            total_size += child_size

                            entry_path = Path(entry.path)

                            folder_sizes[
                                entry_path
                            ] = child_size

                            if folder_name in SPECIAL_FOLDERS:

                                special_folders.append({
                                    "name": SPECIAL_FOLDERS[
                                        folder_name
                                    ],
                                    "path": entry_path,
                                    "size": child_size
                                })

                            if (
                                folder_name in TEMP_FOLDER_NAMES
                                and child_size >= MIN_CACHE_SIZE
                            ):

                                cache_folders.append({
                                    "name":
                                        "Temporary / Cache Folder",
                                    "path": entry_path,
                                    "size": child_size
                                })

                            continue

                        if not entry.is_file(
                            follow_symlinks=False
                        ):
                            continue

                        stat = entry.stat(
                            follow_symlinks=False
                        )

                        size = stat.st_size
                        total_size += size

                        # Files inside ignored directories
                        # still count toward total storage,
                        # but are excluded from detailed analysis.

                        if ignored:
                            continue

                        entry_path = Path(entry.path)

                        modified_timestamp = stat.st_mtime

                        modified = datetime.fromtimestamp(
                            modified_timestamp
                        )

                        category = get_file_category(
                            entry_path
                        )

                        file_data = {
                            "path": entry_path,
                            "size": size,
                            "modified": modified,
                            "category": category
                        }

                        files.append(file_data)

                        # Large files

                        if size >= MIN_LARGE_FILE_SIZE:

                            large_file_data = {
                                "name": entry.name,
                                "path": entry_path,
                                "size": size,
                                "modified": modified,
                                "category": category
                            }

                            add_large_file(
                                large_file_data
                            )

                        # Old files

                        if modified_timestamp < cutoff_timestamp:

                            old_file_data = {
                                "name": entry.name,
                                "path": entry_path,
                                "size": size,
                                "modified": modified,
                                "category": category
                            }

                            add_old_file(
                                old_file_data
                            )

                        # Categories

                        category_sizes[category] = (
                            category_sizes.get(category, 0)
                            + size
                        )

                        # Duplicate candidates

                        if size >= MIN_DUPLICATE_SIZE:

                            if size not in duplicate_candidates:
                                duplicate_candidates[size] = []

                            duplicate_candidates[
                                size
                            ].append(entry_path)

                    except (
                        PermissionError,
                        OSError,
                        ValueError
                    ):
                        continue

        except (
            PermissionError,
            OSError
        ):
            return 0

        return total_size

    total_size = scan_directory(
        root
    )

    folder_sizes[root] = total_size

    # Convert largest files heap to sorted list.

    large_files = [
        item[1]
        for item in large_files_heap
    ]

    large_files.sort(
        key=lambda file: file["size"],
        reverse=True
    )

    # Convert old files heap to sorted list.

    old_files = [
        item[1]
        for item in old_files_heap
    ]

    old_files.sort(
        key=lambda file: file["size"],
        reverse=True
    )

    # Sort special folders.

    special_folders.sort(
        key=lambda folder: folder["size"],
        reverse=True
    )

    special_folders = special_folders[
        :MAX_SPECIAL_FOLDERS
    ]

    # Sort cache folders.

    cache_folders.sort(
        key=lambda folder: folder["size"],
        reverse=True
    )

    cache_folders = cache_folders[
        :MAX_CACHE_FOLDERS
    ]

    # Category results.

    category_results = [
        {
            "category": category,
            "size": size
        }
        for category, size in category_sizes.items()
    ]

    category_results.sort(
        key=lambda item: item["size"],
        reverse=True
    )

    # Keep only actual duplicate candidates.

    duplicate_candidates = {
        size: paths
        for size, paths in duplicate_candidates.items()
        if len(paths) >= 2
    }

    # Top-level folders.
    # Their sizes were already calculated during
    # the main scan, so no second filesystem scan is needed.

    top_level_folders = []

    try:
        with os.scandir(root) as entries:

            for entry in entries:

                try:

                    if entry.is_dir(
                        follow_symlinks=False
                    ) and not entry.is_symlink():

                        path = Path(entry.path)

                        top_level_folders.append({
                            "name": entry.name,
                            "path": path,
                            "size": folder_sizes.get(
                                path,
                                0
                            )
                        })

                except (
                    PermissionError,
                    OSError
                ):
                    continue

    except (
        PermissionError,
        OSError
    ):
        pass

    top_level_folders.sort(
        key=lambda folder: folder["size"],
        reverse=True
    )

    return {
        "root": root,
        "total_size": total_size,
        "files": files,
        "folder_sizes": folder_sizes,
        "top_level_folders": top_level_folders,
        "large_files": large_files,
        "old_files": old_files,
        "categories": category_results,
        "special_folders": special_folders,
        "cache_folders": cache_folders,
        "duplicate_candidates": duplicate_candidates
    }