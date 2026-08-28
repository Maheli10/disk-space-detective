import psutil

partitions = psutil.disk_partitions()

for partition in partitions:
    drive = partition.mountpoint
    usage = psutil.disk_usage(drive)

    print("Drive:", drive)
    print("Total:", usage.total)
    print("Used:", usage.used)
    print("Free:", usage.free)
    print()