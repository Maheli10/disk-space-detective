import psutil


def get_disks():
    """Return available disk partitions."""
    return psutil.disk_partitions()

def get_disk_status(used_percent):
    if used_percent < 70:
        return "Healthy"
    elif used_percent < 85:
        return "Moderate"
    elif used_percent < 95:
        return "Warning"
    else:
        return "Critical"


def scan_disk(disk_index):
    """Scan a selected disk and return its information."""

    partitions = get_disks()

    if disk_index < 0 or disk_index >= len(partitions):
        raise ValueError("Invalid disk index.")

    partition = partitions[disk_index]
    drive = partition.mountpoint

    try:
        usage = psutil.disk_usage(drive)
    except OSError:
        return{
            "drive":drive,
            "error":"Unble to access drives "
        }
    status=get_disk_status(usage.percent)

    return {
        "drive": drive,
        "total": usage.total,
        "used": usage.used,
        "free": usage.free,
        "used_percent": usage.percent,
        "status":status
    }