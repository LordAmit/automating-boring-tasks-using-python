#!/usr/bin/env python3
import sys
import subprocess
import shlex
from typing import List
if __name__ == "__main__":
    if len(sys.argv) == 2:
        apk_package: str = sys.argv[1]
        command = "adb shell pm path {}".format(apk_package)
        # print(command)
        lines: List[str] = subprocess.check_output(
            shlex.split(command)).decode("utf-8").splitlines()
        # print(lines[0])
        apk_path = lines[0][8:]
        print(apk_path)
        cmd_pull_apk: str = "adb pull {} {}.apk".format(apk_path, apk_package)
        print(cmd_pull_apk)
        subprocess.check_output(shlex.split(cmd_pull_apk))
