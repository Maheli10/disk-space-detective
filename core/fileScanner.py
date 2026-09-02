from pathlib import Path


def get_large_files(folder_path, min_size=100 * 1024 * 1024):
    """Find the 10 largest files above the minimum size."""

    folder = Path(folder_path)
    large_files = []

    for item in folder.rglob("*"):

        try:
            if item.is_file():

                size = item.stat().st_size

                if size >= min_size:
                    large_files.append((item, size))

        except (PermissionError, OSError):
            continue

    # Sort files from largest to smallest
    large_files.sort(key=lambda file: file[1], reverse=True)

    # Return only the 10 largest files
    return large_files[:10]