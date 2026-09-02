from diskScanner import get_disks, scan_disk
from folderScanner import get_folder_size


def format_size(size):
    """Convert bytes into a readable size."""

    if size >= 1024 ** 3:
        return f"{size / (1024 ** 3):.2f} GB"

    if size >= 1024 ** 2:
        return f"{size / (1024 ** 2):.2f} MB"

    if size >= 1024:
        return f"{size / 1024:.2f} KB"

    return f"{size} bytes"


def main():
    print("=" * 45)
    print("          DISK SPACE DETECTIVE")
    print("=" * 45)

    # Find available disks
    disks = get_disks()

    print("\nAvailable Disks:")

    for index, disk in enumerate(disks):
        print(f"  {index}. {disk.mountpoint}")

    # Scan the first disk
    if disks:
        result = scan_disk(0)

        print("\nDisk Information:")
        print(f"  Drive       : {result['drive']}")
        print(f"  Total Space : {format_size(result['total'])}")
        print(f"  Used Space  : {format_size(result['used'])}")
        print(f"  Free Space  : {format_size(result['free'])}")
        print(f"  Used        : {result['used_percent']}%")

    # Test folder scanner
    folder = "C:/Users"
    size = get_folder_size(folder)

    print("\nFolder Information:")
    print(f"  Folder      : {folder}")
    print(f"  Total Size  : {format_size(size)}")

    print("\n" + "=" * 45)
    print("       Scan completed successfully!")
    print("=" * 45)


if __name__ == "__main__":
    main()