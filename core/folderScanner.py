from pathlib import Path


def get_folder_size(folder_path):
    """Calculate the total size of all files inside a folder."""

    folder = Path(folder_path)
    total_size = 0

    for item in folder.rglob("*"):
        try:
            if item.is_file():
                total_size += item.stat().st_size

        except (PermissionError, OSError):
            continue

    return total_size


def get_subfolders(folder_path):
    """Return all folders directly inside the given folder."""

    folder = Path(folder_path)
    subfolders = []

    try:
        for item in folder.iterdir():

            if item.is_dir():
                subfolders.append(item)

    except (PermissionError, OSError):
        pass

    return subfolders