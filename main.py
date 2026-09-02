from diskScanner import get_disks, scan_disk
from folderScanner import get_folder_size, get_subfolders


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
    """Scan all folders inside a drive."""

    print(f"\nDRIVE: {drive}")
    print("-" * 45)

    folders = get_subfolders(drive)

    if not folders:
        print("No accessible folders found.")
        return

    for folder in folders:

        size = get_folder_size(folder)

        print(f"  {folder.name:<25} {format_size(size)}")


def main():

    print("=" * 45)
    print("          DISK SPACE DETECTIVE")
    print("=" * 45)

    # ------------------------------------------------
    # 1. Find available disks
    # ------------------------------------------------

    disks = get_disks()

    print("\nAvailable Disks:")

    for index, disk in enumerate(disks):
        print(f"  {index}. {disk.mountpoint}")

    # ------------------------------------------------
    # 2. Show disk information for every disk
    # ------------------------------------------------

    for index, disk in enumerate(disks):

        result = scan_disk(index)

        print(f"\nDisk Information - {result['drive']}:")
        print(f"  Total Space : {format_size(result['total'])}")
        print(f"  Used Space  : {format_size(result['used'])}")
        print(f"  Free Space  : {format_size(result['free'])}")
        print(f"  Used        : {result['used_percent']}%")

    # ------------------------------------------------
    # 3. Scan folders inside every disk
    # ------------------------------------------------

    print("\n" + "=" * 45)
    print("             FOLDER ANALYSIS")
    print("=" * 45)

    for disk in disks:

        drive = disk.mountpoint

        scan_drive(drive)

    # ------------------------------------------------
    # 4. Scan completed
    # ------------------------------------------------

    print("\n" + "=" * 45)
    print("       Scan completed successfully!")
    print("=" * 45)


if __name__ == "__main__":
    main()

