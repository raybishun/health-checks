#!/usr/bin/env python3
import os
import shutil
import sys

def check_reboot():
    """Returns True if the computer has a pending reboot."""
    return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_gb, min_percent):
    """Return True if insufficient free space, else return False."""
    du = shutil.disk_usage(disk)
    # Calc % of free space
    precent_free = 100 * du.free / du.total
    # Calc GB of free space
    gigabytes_free = du.free / 2 ** 30
    if gigabytes_free < min_gb or precent_free < min_percent:
        return True
    return False        

def main():
    if check_reboot():
        print("Pending Reboot.")
        sys.exit(1)
    if check_disk_full(disk="/", min_gb=2, min_percent=10):
        print("Disk full!")
        sys.exit(1)
    print("All Clear!")
    sys.exit(0)

main()