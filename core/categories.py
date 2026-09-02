from pathlib import Path


def get_file_category(file_path):
    """Return a category based on the file extension."""

    extension = Path(file_path).suffix.lower()

    if extension in [".mp4", ".mkv", ".avi", ".mov", ".wmv"]:
        return "Video"

    elif extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
        return "Image"

    elif extension in [".mp3", ".wav", ".flac", ".aac"]:
        return "Audio"

    elif extension in [".zip", ".rar", ".7z", ".tar", ".gz"]:
        return "Archive"

    elif extension in [".exe", ".msi"]:
        return "Application"

    elif extension in [".py", ".js", ".java", ".cpp", ".c", ".html", ".css"]:
        return "Code"

    elif extension in [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx"]:
        return "Document"

    else:
        return "Other"


