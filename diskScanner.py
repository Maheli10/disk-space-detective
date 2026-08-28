import psutil


def get_disks():
    """Return available disk partitions."""
    return psutil.disk_partitions()


def scan_disk(disk_index):
    """Scan a selected disk and return its information."""

    partitions = get_disks()

    if disk_index < 0 or disk_index >= len(partitions):
        raise ValueError("Invalid disk index.")

    partition = partitions[disk_index]
    drive = partition.mountpoint

    usage = psutil.disk_usage(drive)

    return {
        "drive": drive,
        "total": usage.total,
        "used": usage.used,
        "free": usage.free,
        "used_percent": usage.percent
    }