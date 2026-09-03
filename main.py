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

from core.recommendations import generate_all_recommendations


def format_size(size):
    """Convert bytes into a readable size."""

    if size >= 1024 ** 3:
        return f"{size / (1024 ** 3):.2f} GB"

    if size >= 1024 ** 2:
        return f"{size / (1024 ** 2):.2f} MB"

    if size >= 1024:
        return f"{size / 1024:.2f} KB"

    return f"{size} bytes"


def run_quick_scan(drive):
    """Run a fast scan for basic disk information and large files."""

    print("\n")
    print("=" * 45)
    print("              QUICK SCAN")
    print("=" * 45)

    print(f"\nDrive: {drive}")
    print("-" * 45)

    # Get basic disk information

    disks = get_disks()

    selected_disk = None

    for disk in disks:
        if disk.mountpoint == drive:
            selected_disk = disk
            break

    if selected_disk is None:
        print("Unable to find selected drive.")
        return

    usage = scan_disk(
        disks.index(selected_disk)
    )

    print("\nDISK INFORMATION")
    print("-" * 45)

    print(
        f"  Total Space : "
        f"{format_size(usage['total'])}"
    )

    print(
        f"  Used Space  : "
        f"{format_size(usage['used'])}"
    )

    print(
        f"  Free Space  : "
        f"{format_size(usage['free'])}"
    )

    print(
        f"  Used        : "
        f"{usage['used_percent']}%"
    )

    # Find large files

    print("\nLARGEST FILES")
    print("-" * 45)

    print("  Minimum size: 100 MB")
    print("  Maximum results: 10")

    large_files = get_large_files(
        drive,
        min_size=100 * 1024 * 1024,
        limit=10
    )

    if not large_files:
        print("\n  No files larger than 100 MB found.")
    else:
        for index, (file, size) in enumerate(
            large_files,
            start=1
        ):
            category = get_file_category(file)

            print(f"\n  {index}. {file.name}")

            print(
                f"     Location: "
                f"{file.parent}"
            )

            print(
                f"     Category: "
                f"{category}"
            )

            print(
                f"     Size: "
                f"{format_size(size)}"
            )

    print("\n" + "=" * 45)
    print("       Quick scan completed!")
    print("=" * 45)


def scan_drive(drive):
    """Scan folders and large files inside a drive."""

    print(f"\nDRIVE: {drive}")
    print("-" * 45)

    folders = get_subfolders(drive)

    if not folders:
        print("No accessible folders found.")
        return

    print("\nFolders:")
    print("-" * 45)

    for folder in folders:
        size = get_folder_size(folder)

        print(
            f"  {folder.name:<25} "
            f"{format_size(size)}"
        )

    print("\nLargest Files:")
    print("-" * 45)

    large_files = get_large_files(drive)

    if not large_files:
        print("  No large files found.")
        return

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
                print(f"        {file}")
    else:
        print(
            "  No meaningful duplicate "
            "files found."
        )

    return {
        "special": special_results,
        "temporary": temp_results,
        "duplicates": duplicate_results
    }


def show_smart_analysis(drive):
    """Show smart analysis of storage usage."""

    print("\n")
    print("=" * 45)
    print("             SMART ANALYSIS")
    print("=" * 45)

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

    return {
        "folders": folders,
        "categories": categories,
        "old_files": old_files
    }


def show_recommendations(
    drive,
    smart_results,
    detective_results
):
    """Show recommendations using existing scan results."""

    print("\n")
    print("=" * 45)
    print("           RECOMMENDATIONS")
    print("=" * 45)

    folders = smart_results["folders"]
    old_files = smart_results["old_files"]

    duplicates = detective_results["duplicates"]
    temp_folders = detective_results["temporary"]

    recommendations = generate_all_recommendations(
        folders=folders,
        duplicates=duplicates,
        old_files=old_files,
        temp_folders=temp_folders
    )

    if not recommendations:
        print("\n  No recommendations at this time.")
        return

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):
        print(
            f"\n  {index}. "
            f"{recommendation['type']}"
        )

        print(
            f"     {recommendation['message']}"
        )

        print(
            f"     Related size: "
            f"{format_size(recommendation['size'])}"
        )


def main():

    print("=" * 45)
    print("          DISK SPACE DETECTIVE")
    print("=" * 45)

    # 1. Find available disks

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

    # 2. Run Quick Scan

    print("\n" + "=" * 45)
    print("             SCAN MODE")
    print("=" * 45)

    print("\n  1. Quick Scan")
    print("  2. Full Scan")

    choice = input("\nSelect scan mode: ").strip()

    if choice not in {"1", "2"}:
        print("\nInvalid choice.")
        return

    # Select drive

    print("\nAvailable Drives:")

    for index, disk in enumerate(disks):
        print(
            f"  {index}. "
            f"{disk.mountpoint}"
        )

    drive_choice = input(
        "\nSelect drive: "
    ).strip()

    try:
        drive_index = int(drive_choice)

        if drive_index < 0 or drive_index >= len(disks):
            print("\nInvalid drive selection.")
            return

    except ValueError:
        print("\nPlease enter a valid number.")
        return

    drive = disks[drive_index].mountpoint

    # Quick Scan

    if choice == "1":

        run_quick_scan(drive)
        return

    # 3. Show disk information

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

    # 4. Storage analysis

    print("\n" + "=" * 45)
    print("             STORAGE ANALYSIS")
    print("=" * 45)

    scan_drive(drive)

    # 5, 6 and 7. Findings, analysis and recommendations

    detective_results = show_detective_findings(drive)

    smart_results = show_smart_analysis(drive)

    show_recommendations(
        drive,
        smart_results,
        detective_results
    )

    # 8. Scan completed

    print("\n" + "=" * 45)
    print("       Full scan completed successfully!")
    print("=" * 45)


if __name__ == "__main__":
    main()