#!/usr/bin/env python3 

import subprocess
import os

APKANALYZER = "/Users/amitseal/Android/Sdk/tools/bin/apkanalyzer"
APKANALYZER_COMMAND = "{} dex list {}"


def is_multidex(apk_path: str):
    global APKANALYZER
    global APKANALYZER_COMMAND
    # command = shlex.split(APKANALYZER_COMMAND.format(APKANALYZER, apk_path))
    command = APKANALYZER_COMMAND.format(APKANALYZER, apk_path)
    print(command)
    output = subprocess.getoutput(command)
    lines = output.splitlines()
    count_dex = 0
    for line in lines:
        if line.endswith(".dex"):
            count_dex += 1
        if count_dex >= 2:
            return True
    return False


def count_multidex_in_dir(dir_path: str):
    apk_count = 0
    multidex_count = 0
    for entry in os.scandir(dir_path):
        if entry.is_file():
            file_name: str = entry.name
            if file_name.endswith(".apk"):
                apk_count += 1
                if is_multidex(dir_path+os.sep+file_name):
                    multidex_count += 1
    return (multidex_count, apk_count)


if __name__ == "__main__":
    print(count_multidex_in_dir("/Users/amitseal/workspaces/apks"))