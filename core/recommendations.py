from pathlib import Path


# ------------------------------------------------
# Folder recommendations
# ------------------------------------------------

def generate_folder_recommendations(folders):
    """
    Generate recommendations based on large folders.
    """

    recommendations = []

    for folder in folders:

        name = folder["name"].lower()
        size = folder["size"]
        path = folder["path"]

        # -----------------------------------------
        # Node modules
        # -----------------------------------------

        if name == "node_modules":

            recommendations.append({
                "type": "Node Modules",
                "message": (
                    f"{path} is using a large amount of space. "
                    "node_modules can usually be regenerated "
                    "using npm install."
                ),
                "size": size
            })

        # -----------------------------------------
        # Python virtual environments
        # -----------------------------------------

        elif name in {"venv", ".venv"}:

            recommendations.append({
                "type": "Python Environment",
                "message": (
                    f"{path} is using storage as a Python "
                    "virtual environment. Review whether "
                    "this environment is still needed."
                ),
                "size": size
            })

    return recommendations


# ------------------------------------------------
# Duplicate recommendations
# ------------------------------------------------

def generate_duplicate_recommendations(duplicates):
    """
    Generate recommendations for duplicate files.
    """

    recommendations = []

    for duplicate in duplicates:

        files = duplicate["files"]
        size = duplicate["size"]

        wasted_space = size * (len(files) - 1)

        recommendations.append({
            "type": "Duplicate Files",
            "message": (
                f"{len(files)} identical files were found. "
                "Consider keeping one copy and removing "
                "unnecessary duplicates."
            ),
            "size": wasted_space
        })

    return recommendations


# ------------------------------------------------
# Old file recommendations
# ------------------------------------------------

def generate_old_file_recommendations(old_files):
    """
    Generate recommendations for old files.
    """

    recommendations = []

    for file in old_files:

        recommendations.append({
            "type": "Old File",
            "message": (
                f"{file['path']} has not been modified "
                "for a long time. Review whether it is "
                "still needed."
            ),
            "size": file["size"]
        })

    return recommendations


# ------------------------------------------------
# Temporary / cache recommendations
# ------------------------------------------------

def generate_temporary_recommendations(temp_folders):
    """
    Generate recommendations for temporary or cache folders.
    """

    recommendations = []

    for folder in temp_folders:

        recommendations.append({
            "type": "Temporary / Cache",
            "message": (
                f"{folder['path']} appears to contain "
                "temporary or cached data. Review whether "
                "it can be safely cleared."
            ),
            "size": folder["size"]
        })

    return recommendations


# ------------------------------------------------
# Combine all recommendations
# ------------------------------------------------

def generate_all_recommendations(
    folders=None,
    duplicates=None,
    old_files=None,
    temp_folders=None
):
    """
    Generate all storage recommendations.
    """

    recommendations = []

    if folders:
        recommendations.extend(
            generate_folder_recommendations(folders)
        )

    if duplicates:
        recommendations.extend(
            generate_duplicate_recommendations(duplicates)
        )

    if old_files:
        recommendations.extend(
            generate_old_file_recommendations(old_files)
        )

    if temp_folders:
        recommendations.extend(
            generate_temporary_recommendations(temp_folders)
        )

    # Sort recommendations by the amount of
    # storage they could potentially save.
    recommendations.sort(
        key=lambda item: item["size"],
        reverse=True
    )

    return recommendations