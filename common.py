"""Common functions for cluster operations"""

import subprocess


def run_command(cmd: list[str]):
    cp = subprocess.run(cmd, capture_output=True)
    split_out = cp.stdout.decode().split("\n")
    split_err = cp.stderr.decode().split("\n")

    for line in split_out:
        print(line)

    for line in split_err:
        print(line)

    if cp.returncode:
        raise Exception("Cluster operation failed - review output above")
