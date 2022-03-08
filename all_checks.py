#!/usr/bin/env python
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
def check_root_full():
    """Returns True if the root part is full, else returns False."""
    return check_disk_full(disk="/", min_gb=2, min_percent=10)
def main():
    checks=[
        (check_reboot, "Pending Reboot"),
        (check_root_full, "Root partition full")
    ]
    everything_ok = True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False
        if not everything_ok:
            sys.exit(1)   
    print("All Clear!")
    sys.exit(0)
main()