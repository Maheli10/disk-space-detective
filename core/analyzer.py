from pathlib import Path
from core.categories import get_file_category


def analyze_files(folder_path):
    """Calculate total storage used by each file category."""

    folder = Path(folder_path)

    category_sizes = {}

    for item in folder.rglob("*"):

        try:
            if item.is_file():

                size = item.stat().st_size
                category = get_file_category(item)

                if category not in category_sizes:
                    category_sizes[category] = 0

                category_sizes[category] += size

        except (PermissionError, OSError):
            continue

    return category_sizes
