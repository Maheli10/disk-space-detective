from pathlib import Path
import hashlib

from core.folderScanner import get_folder_size


# Folders ignored ONLY when searching for duplicates.
# These folders normally contain many repeated files.
IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__"
}


# Folders that are interesting for our investigation.
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


# Only consider duplicate files that are at least 1 MB.
MIN_DUPLICATE_SIZE = 1 * 1024 * 1024


def should_ignore(path):
    """Check whether a path is inside an ignored directory."""

    return any(
        part in IGNORED_DIRECTORIES
        for part in path.parts
    )


def detect_special_folders(folder_path):
    """Find special folders that may consume significant storage."""

    folder = Path(folder_path)

    findings = []

    for item in folder.rglob("*"):

        try:

            if item.is_dir() and item.name in SPECIAL_FOLDERS:

                findings.append({
                    "name": SPECIAL_FOLDERS[item.name],
                    "path": item,
                    "size": get_folder_size(item)
                })

        except (PermissionError, OSError):
            continue

    return findings


def detect_temporary_folders(folder_path):
    """Find folders that appear to contain temporary or cached data."""

    folder = Path(folder_path)

    findings = []

    for item in folder.rglob("*"):

        try:

            if (
                item.is_dir()
                and item.name.lower() in TEMP_FOLDER_NAMES
            ):

                findings.append({
                    "name": "Temporary / Cache Folder",
                    "path": item,
                    "size": get_folder_size(item)
                })

        except (PermissionError, OSError):
            continue

    return findings


def calculate_file_hash(file_path, chunk_size=1024 * 1024):
    """
    Calculate the SHA-256 hash of a file.

    The file is read in chunks instead of loading
    the entire file into memory.
    """

    sha256 = hashlib.sha256()

    try:

        with open(file_path, "rb") as file:

            while True:

                chunk = file.read(chunk_size)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    except (PermissionError, OSError):

        return None


def find_duplicates(folder_path):
    """
    Find actual duplicate files.

    Only files >= 1 MB are considered.

    Files are first grouped by size.
    Files with the same size are then hashed.
    Files with the same SHA-256 hash are duplicates.
    """

    folder = Path(folder_path)

    size_groups = {}

    # ---------------------------------------------
    # Step 1: Group files by size
    # ---------------------------------------------

    for item in folder.rglob("*"):

        try:

            if item.is_file():

                # Ignore generated/dependency folders
                if should_ignore(item):
                    continue

                size = item.stat().st_size

                # Ignore small files
                if size < MIN_DUPLICATE_SIZE:
                    continue

                if size not in size_groups:
                    size_groups[size] = []

                size_groups[size].append(item)

        except (PermissionError, OSError):
            continue

    # ---------------------------------------------
    # Step 2: Compare files with the same size
    # ---------------------------------------------

    duplicates = []

    for size, files in size_groups.items():

        # One file cannot be a duplicate
        if len(files) < 2:
            continue

        hash_groups = {}

        for file in files:

            file_hash = calculate_file_hash(file)

            if file_hash:

                if file_hash not in hash_groups:
                    hash_groups[file_hash] = []

                hash_groups[file_hash].append(file)

        # -----------------------------------------
        # Step 3: Find files with the same hash
        # -----------------------------------------

        for file_hash, matching_files in hash_groups.items():

            if len(matching_files) > 1:

                duplicates.append({
                    "size": size,
                    "hash": file_hash,
                    "files": matching_files
                })

    # ---------------------------------------------
    # Sort largest wasted space first
    # ---------------------------------------------

    duplicates.sort(
        key=lambda result:
        result["size"] * (len(result["files"]) - 1),
        reverse=True
    )

    return duplicates


def format_size(size):
    """Convert bytes into a readable size."""

    if size >= 1024 ** 3:
        return f"{size / (1024 ** 3):.2f} GB"

    if size >= 1024 ** 2:
        return f"{size / (1024 ** 2):.2f} MB"

    if size >= 1024:
        return f"{size / 1024:.2f} KB"

    return f"{size} bytes"


# ------------------------------------------------
# Test the detector
# ------------------------------------------------

if __name__ == "__main__":

    test_folder = r"D:\Github repo"

    print("=" * 50)
    print("           DISK SPACE DETECTIVE")
    print("=" * 50)

    # ---------------------------------------------
    # Special folders
    # ---------------------------------------------

    print("\nSPECIAL FOLDERS")
    print("-" * 50)

    special_results = detect_special_folders(test_folder)

    if special_results:

        for result in special_results:

            print(f"\n{result['name']}")
            print(f"  Location : {result['path']}")
            print(f"  Size     : {format_size(result['size'])}")

    else:

        print("No special folders found.")

    # ---------------------------------------------
    # Temporary / cache folders
    # ---------------------------------------------

    print("\nTEMPORARY / CACHE FOLDERS")
    print("-" * 50)

    temp_results = detect_temporary_folders(test_folder)

    if temp_results:

        for result in temp_results:

            print(f"\n{result['name']}")
            print(f"  Location : {result['path']}")
            print(f"  Size     : {format_size(result['size'])}")

    else:

        print("No temporary or cache folders found.")

    # ---------------------------------------------
    # Actual duplicates
    # ---------------------------------------------

    print("\nACTUAL DUPLICATES")
    print("-" * 50)

    duplicate_results = find_duplicates(test_folder)

    if duplicate_results:

        print(f"\nFound {len(duplicate_results)} duplicate groups.")

        for index, result in enumerate(
            duplicate_results,
            start=1
        ):

            files = result["files"]
            file_size = result["size"]

            wasted_space = file_size * (len(files) - 1)

            print(f"\n{index}. {files[0].name}")
            print(f"   Copies       : {len(files)}")
            print(f"   File size    : {format_size(file_size)}")
            print(f"   Wasted space : {format_size(wasted_space)}")

            for file in files:
                print(f"      {file}")

    else:

        print("No meaningful duplicate files found.")

    print("\n" + "=" * 50)
    print("              Scan completed")
    print("=" * 50)