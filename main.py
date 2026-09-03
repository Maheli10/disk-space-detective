from core.diskScanner import get_disks, scan_disk
from core.folderScanner import get_folder_size, get_subfolders
from core.fileScanner import get_large_files
from core.categories import get_file_category

from core.detector import (
    detect_special_folders,
    detect_temporary_folders,
    find_duplicates
)

from core.analyzer import (
    analyze_folders,
    analyze_file_categories,
    find_old_files
)


def format_size(size):
    """Convert bytes into a readable size."""

    if size >= 1024 ** 3:
        return f"{size / (1024 ** 3):.2f} GB"

    if size >= 1024 ** 2:
        return f"{size / (1024 ** 2):.2f} MB"

    if size >= 1024:
        return f"{size / 1024:.2f} KB"

    return f"{size} bytes"


def scan_drive(drive):
    """Scan all folders and large files inside a drive."""

    print(f"\nDRIVE: {drive}")
    print("-" * 45)

    folders = get_subfolders(drive)

    if not folders:
        print("No accessible folders found.")
        return

    # ---------------------------------------------
    # Show folder sizes
    # ---------------------------------------------

    print("\nFolders:")
    print("-" * 45)

    for folder in folders:

        size = get_folder_size(folder)

        print(
            f"  {folder.name:<25} "
            f"{format_size(size)}"
        )

    # ---------------------------------------------
    # Show largest files
    # ---------------------------------------------

    print("\nLargest Files:")
    print("-" * 45)

    large_files = get_large_files(drive)

    if not large_files:

        print("  No large files found.")

    else:

        for index, (file, size) in enumerate(
            large_files,
            start=1
        ):

            category = get_file_category(file)

            print(f"\n  {index}. {file.name}")
            print(f"     Location: {file.parent}")
            print(f"     Category: {category}")
            print(f"     Size: {format_size(size)}")


def show_detective_findings(drive):
    """Show intelligent findings about storage usage."""

    print("\n")
    print("=" * 45)
    print("           DETECTIVE FINDINGS")
    print("=" * 45)

    # ---------------------------------------------
    # Special folders
    # ---------------------------------------------

    print("\nSPECIAL FOLDERS")
    print("-" * 45)

    special_results = detect_special_folders(drive)

    if special_results:

        for result in special_results:

            print(f"\n  {result['name']}")
            print(f"  Location: {result['path']}")
            print(
                f"  Size: "
                f"{format_size(result['size'])}"
            )

    else:

        print("  No special folders found.")

    # ---------------------------------------------
    # Temporary / cache folders
    # ---------------------------------------------

    print("\nTEMPORARY / CACHE")
    print("-" * 45)

    temp_results = detect_temporary_folders(drive)

    if temp_results:

        for result in temp_results:

            print(f"\n  {result['name']}")
            print(f"  Location: {result['path']}")
            print(
                f"  Size: "
                f"{format_size(result['size'])}"
            )

    else:

        print("  No temporary or cache folders found.")

    # ---------------------------------------------
    # Actual duplicate files
    # ---------------------------------------------

    print("\nACTUAL DUPLICATES")
    print("-" * 45)

    duplicate_results = find_duplicates(drive)

    if duplicate_results:

        print(
            f"  Found {len(duplicate_results)} "
            f"duplicate groups."
        )

        for index, result in enumerate(
            duplicate_results[:10],
            start=1
        ):

            files = result["files"]
            file_size = result["size"]

            wasted_space = (
                file_size * (len(files) - 1)
            )

            print(
                f"\n  {index}. "
                f"{files[0].name}"
            )

            print(
                f"     Copies: "
                f"{len(files)}"
            )

            print(
                f"     File size: "
                f"{format_size(file_size)}"
            )

            print(
                f"     Wasted space: "
                f"{format_size(wasted_space)}"
            )

            for file in files:

                print(
                    f"        {file}"
                )

    else:

        print(
            "  No meaningful duplicate "
            "files found."
        )


def show_smart_analysis(drive):
    """Show smart analysis of storage usage."""

    print("\n")
    print("=" * 45)
    print("             SMART ANALYSIS")
    print("=" * 45)

    # ---------------------------------------------
    # Biggest folders
    # ---------------------------------------------

    print("\nBIGGEST FOLDERS")
    print("-" * 45)

    folders = analyze_folders(drive)

    if folders:

        for index, folder in enumerate(
            folders,
            start=1
        ):

            print(
                f"\n  {index}. "
                f"{folder['name']}"
            )

            print(
                f"     Size: "
                f"{format_size(folder['size'])}"
            )

            print(
                f"     Location: "
                f"{folder['path']}"
            )

    else:

        print("  No folders found.")

    # ---------------------------------------------
    # File categories
    # ---------------------------------------------

    print("\nFILE CATEGORIES")
    print("-" * 45)

    categories = analyze_file_categories(drive)

    if categories:

        for index, category in enumerate(
            categories,
            start=1
        ):

            print(
                f"  {index}. "
                f"{category['category']}: "
                f"{format_size(category['size'])}"
            )

    else:

        print("  No file categories found.")

    # ---------------------------------------------
    # Old files
    # ---------------------------------------------

    print("\nOLD FILES")
    print("-" * 45)

    old_files = find_old_files(drive)

    if old_files:

        for index, file in enumerate(
            old_files,
            start=1
        ):

            print(
                f"\n  {index}. "
                f"{file['name']}"
            )

            print(
                f"     Size: "
                f"{format_size(file['size'])}"
            )

            print(
                f"     Modified: "
                f"{file['modified']}"
            )

            print(
                f"     Location: "
                f"{file['path']}"
            )

    else:

        print("  No old files found.")


def main():

    print("=" * 45)
    print("          DISK SPACE DETECTIVE")
    print("=" * 45)

    # ------------------------------------------------
    # 1. Find available disks
    # ------------------------------------------------

    disks = get_disks()

    if not disks:

        print("\nNo disks found.")
        return

    print("\nAvailable Disks:")

    for index, disk in enumerate(disks):

        print(
            f"  {index}. "
            f"{disk.mountpoint}"
        )

    # ------------------------------------------------
    # 2. Show disk information
    # ------------------------------------------------

    for index, disk in enumerate(disks):

        result = scan_disk(index)

        print(
            f"\nDisk Information - "
            f"{result['drive']}:"
        )

        print(
            f"  Total Space : "
            f"{format_size(result['total'])}"
        )

        print(
            f"  Used Space  : "
            f"{format_size(result['used'])}"
        )

        print(
            f"  Free Space  : "
            f"{format_size(result['free'])}"
        )

        print(
            f"  Used        : "
            f"{result['used_percent']}%"
        )

    # ------------------------------------------------
    # 3. Storage analysis
    # ------------------------------------------------

    print("\n" + "=" * 45)
    print("             STORAGE ANALYSIS")
    print("=" * 45)

    for disk in disks:

        drive = disk.mountpoint

        scan_drive(drive)

    # ------------------------------------------------
    # 4. Detective findings
    # ------------------------------------------------

    for disk in disks:

        drive = disk.mountpoint

        show_detective_findings(drive)

    # ------------------------------------------------
    # 5. Smart analysis
    # ------------------------------------------------

    for disk in disks:

        drive = disk.mountpoint

        show_smart_analysis(drive)

    # ------------------------------------------------
    # 6. Scan completed
    # ------------------------------------------------

    print("\n" + "=" * 45)
    print("       Scan completed successfully!")
    print("=" * 45)


if __name__ == "__main__":
    main()