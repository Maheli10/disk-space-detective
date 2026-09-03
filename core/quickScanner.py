import os
import heapq
from pathlib import Path

from core.diskScanner import scan_disk


MAX_FOLDERS = 3
MAX_FILES = 3
MIN_LARGE_FILE_SIZE = 100 * 1024 * 1024

SPECIAL_FOLDERS = {
    "node_modules": "Node Modules",
    "venv": "Python Virtual Environment",
    ".venv": "Python Virtual Environment",
    "__pycache__": "Python Cache",
}

TEMP_FOLDER_NAMES = {
    "temp",
    "tmp",
    "cache",
}


def quick_scan(folder_path):

    root = Path(folder_path)

    if not root.exists():
        raise ValueError(f"Folder does not exist: {root}")

    if not root.is_dir():
        raise ValueError(f"Path is not a directory: {root}")

    folder_heap = []
    file_heap = []
    special_folders = []

    def add_folder(path, size):

        item = (size, str(path), path)

        if len(folder_heap) < MAX_FOLDERS:
            heapq.heappush(folder_heap, item)

        elif size > folder_heap[0][0]:
            heapq.heapreplace(folder_heap, item)

    def add_file(path, size):

        item = (size, str(path), path)

        if len(file_heap) < MAX_FILES:
            heapq.heappush(file_heap, item)

        elif size > file_heap[0][0]:
            heapq.heapreplace(file_heap, item)

    def scan_directory(directory):

        total_size = 0

        try:
            with os.scandir(directory) as entries:

                for entry in entries:

                    try:

                        if entry.is_symlink():
                            continue

                        if entry.is_dir(follow_symlinks=False):

                            folder_name = entry.name.lower()

                            size = scan_directory(entry.path)

                            total_size += size

                            path = Path(entry.path)

                            add_folder(path, size)

                            if folder_name in SPECIAL_FOLDERS:
                                special_folders.append({
                                    "name": SPECIAL_FOLDERS[folder_name],
                                    "path": path,
                                    "size": size
                                })

                            elif folder_name in TEMP_FOLDER_NAMES:
                                if size >= 10 * 1024 * 1024:
                                    special_folders.append({
                                        "name": "Temporary / Cache",
                                        "path": path,
                                        "size": size
                                    })

                            continue

                        if not entry.is_file(follow_symlinks=False):
                            continue

                        stat = entry.stat(
                            follow_symlinks=False
                        )

                        size = stat.st_size
                        total_size += size

                        if size >= MIN_LARGE_FILE_SIZE:
                            add_file(
                                Path(entry.path),
                                size
                            )

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

    total_size = scan_directory(root)

    top_folders = [
        {
            "name": item[2].name,
            "path": item[2],
            "size": item[0]
        }
        for item in folder_heap
    ]

    top_folders.sort(
        key=lambda folder: folder["size"],
        reverse=True
    )

    top_files = [
        {
            "name": item[2].name,
            "path": item[2],
            "size": item[0]
        }
        for item in file_heap
    ]

    top_files.sort(
        key=lambda file: file["size"],
        reverse=True
    )

    special_folders.sort(
        key=lambda folder: folder["size"],
        reverse=True
    )

    return {
        "root": root,
        "total_size": total_size,
        "top_folders": top_folders,
        "top_files": top_files,
        "special_folders": special_folders[:10]
    }


def quick_scan_drive(disk_index):

    return scan_disk(disk_index)