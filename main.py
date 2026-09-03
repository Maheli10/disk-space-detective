import time

from core.diskScanner import get_disks,get_disk_status
from core.diskScanner import scan_disk
from core.quickScanner import quick_scan
from core.scanner import scan_filesystem
from core.recommendations import generate_all_recommendations


def format_size(size):

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB"
    ]

    size = float(size)

    for unit in units:

        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def select_location():

    partitions = get_disks()

    print("\nAVAILABLE DRIVES")

    for index, partition in enumerate(partitions):

        print(
            f"  {index}. "
            f"{partition.mountpoint}"
        )

    print("  F. Choose a specific folder")

    choice = input("\nSelect location: ").strip()

    if choice.lower() == "f":

        folder = input(
            "Enter folder path: "
        ).strip()

        return folder

    try:

        index = int(choice)

        if index < 0 or index >= len(partitions):
            raise ValueError

        return partitions[index].mountpoint

    except ValueError:

        print("Invalid selection.")
        return None


def show_quick_scan(location):

    print("\n" + "=" * 50)
    print("⚡ QUICK SCAN")
    print("=" * 50)

    print(f"\nScanning: {location}")

    start_time = time.perf_counter()

    try:

        result = quick_scan(location)

    except Exception as error:

        print(f"\nScan failed: {error}")
        return

    elapsed = time.perf_counter() - start_time

    print("\nSTORAGE")
    print("-" * 50)

    try:

        partitions = get_disks()

        matching_drive = None

        for partition in partitions:

            if partition.mountpoint.lower() == str(
                location
            ).lower():

                matching_drive = partition.mountpoint
                break

        if matching_drive:

            disk_info = scan_disk(
                partitions.index(
                    next(
                        p for p in partitions
                        if p.mountpoint == matching_drive
                    )
                )
            )

            print(
                f"Total:       "
                f"{format_size(disk_info['total'])}"
            )

            print(
                f"Used:        "
                f"{format_size(disk_info['used'])}"
            )

            print(
                f"Free:        "
                f"{format_size(disk_info['free'])}"
            )

            print(
                f"Usage:       "
                f"{disk_info['used_percent']}%"
            )
            health=get_disk_status(result['used_percent'])
            print(
                f"Status:      "
                f"{health}")
    # ------------------------------------------------
    # 3. Scan folders inside every disk
    # ------------------------------------------------

    except (
        PermissionError,
        OSError,
        ValueError,
        StopIteration
    ):
        pass

    print("\n📁 TOP 3 LARGEST FOLDERS")
    print("-" * 50)

    if result["top_folders"]:

        for folder in result["top_folders"]:

            print(
                f"{folder['name']:<25} "
                f"{format_size(folder['size'])}"
            )

    else:

        print("No folders found.")

    print("\n📄 TOP 3 LARGE FILES")
    print("-" * 50)

    if result["top_files"]:

        for file in result["top_files"]:

            print(
                f"{file['name']:<25} "
                f"{format_size(file['size'])}"
            )

    else:

        print("No files over 100 MB found.")

    print("\n🔎 QUICK FINDINGS")
    print("-" * 50)

    if result["special_folders"]:

        for folder in result["special_folders"]:

            print(
                f"{folder['name']:<30} "
                f"{format_size(folder['size'])}"
            )

    else:

        print("No notable storage findings.")

    print("\nSUMMARY")
    print("-" * 50)

    print(
        f"Scanned Size: "
        f"{format_size(result['total_size'])}"
    )

    print(
        f"Scan Time: "
        f"{elapsed:.2f} seconds"
    )

    print("\nQuick Scan completed successfully.")


def show_deep_scan(location):

    print("\n" + "=" * 50)
    print("🔎 DEEP SCAN")
    print("=" * 50)

    print(f"\nScanning: {location}")

    start_time = time.perf_counter()

    try:

        result = scan_filesystem(location)

    except Exception as error:

        print(f"\nScan failed: {error}")
        return

    elapsed = time.perf_counter() - start_time

    print("\nSTORAGE")
    print("-" * 50)

    print(
        f"Scanned Size: "
        f"{format_size(result['total_size'])}"
    )

    print(
        f"Scan Time: "
        f"{elapsed:.2f} seconds"
    )

    print("\nLARGEST FOLDERS")
    print("-" * 50)

    if result["top_level_folders"]:

        for folder in result["top_level_folders"][:10]:

            print(
                f"{folder['name']:<25} "
                f"{format_size(folder['size'])}"
            )

    else:

        print("No folders found.")

    print("\nLARGEST FILES")
    print("-" * 50)

    if result["large_files"]:

        for file in result["large_files"]:

            print(
                f"{file['name']:<25} "
                f"{format_size(file['size'])}"
            )

    else:

        print("No large files found.")

    print("\nFILE CATEGORIES")
    print("-" * 50)

    if result["categories"]:

        for category in result["categories"]:

            print(
                f"{category['category']:<20} "
                f"{format_size(category['size'])}"
            )

    else:

        print("No categories found.")

    print("\nOLD FILES")
    print("-" * 50)

    if result["old_files"]:

        for file in result["old_files"]:

            print(
                f"{file['name']:<25} "
                f"{format_size(file['size'])}"
            )

    else:

        print("No old files found.")

    print("\nDETECTIVE FINDINGS")
    print("-" * 50)

    if result["special_folders"]:

        for folder in result["special_folders"]:

            print(
                f"{folder['name']:<30} "
                f"{format_size(folder['size'])}"
            )

            print(
                f"  {folder['path']}"
            )

    else:

        print("No special folders found.")

    print("\nTEMPORARY / CACHE FOLDERS")
    print("-" * 50)

    if result["cache_folders"]:

        for folder in result["cache_folders"]:

            print(
                f"{folder['name']:<30} "
                f"{format_size(folder['size'])}"
            )

    else:

        print("No large temporary/cache folders found.")

    print("\nDUPLICATE CANDIDATES")
    print("-" * 50)

    if result["duplicate_candidates"]:

        for size, paths in result[
            "duplicate_candidates"
        ].items():

            print(
                f"{len(paths)} files with size "
                f"{format_size(size)}"
            )

    else:

        print("No duplicate candidates found.")

    print("\nSUMMARY")
    print("-" * 50)

    print(
        f"Files analyzed:       "
        f"{len(result['files'])}"
    )

    print(
        f"Folders analyzed:     "
        f"{len(result['folder_sizes'])}"
    )

    print(
        f"Large files:          "
        f"{len(result['large_files'])}"
    )

    print(
        f"Old files:            "
        f"{len(result['old_files'])}"
    )

    print(
        f"Special folders:      "
        f"{len(result['special_folders'])}"
    )

    print(
        f"Cache folders:        "
        f"{len(result['cache_folders'])}"
    )

    print(
        f"Duplicate candidates: "
        f"{len(result['duplicate_candidates'])}"
    )

    print("\nDeep Scan completed successfully.")

    recommendations = generate_all_recommendations(
        folders=result["special_folders"],
        duplicates=[],
        old_files=result["old_files"],
        temp_folders=result["cache_folders"]
    )

    print("\nRECOMMENDATIONS")
    print("-" * 50)

    if recommendations:

        for recommendation in recommendations:

            print(
                f"\n{recommendation['type']}"
            )

            print(
                f"{recommendation['message']}"
            )

            print(
                f"Potential space: "
                f"{format_size(recommendation['size'])}"
            )

    else:

        print("No recommendations at this time.")


def main():

    while True:

        print("\n" + "=" * 50)
        print("🕵️ DISK SPACE DETECTIVE")
        print("=" * 50)

        print("\nSCAN MODE")
        print("  1. ⚡ Quick Scan")
        print("  2. 🔎 Deep Scan")
        print("  3. Exit")

        mode = input(
            "\nSelect scan mode: "
        ).strip()

        if mode == "3":
            print("\nGoodbye!")
            break

        if mode not in {"1", "2"}:

            print("\nInvalid option.")
            continue

        location = select_location()

        if location is None:
            continue

        print(
            f"\nSelected location: "
            f"{location}"
        )

        if mode == "1":

            show_quick_scan(location)

        elif mode == "2":

            show_deep_scan(location)


if __name__ == "__main__":
    main()