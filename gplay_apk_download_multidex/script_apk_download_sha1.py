import time
import random
import subprocess
from datetime import datetime
import shlex
from typing import List
import os
import hashlib
import apk_multidex as mdex


# COMMAND = "gplaycli -d {} -c gplaycli.conf"
COMMAND = "{} -d {} -c {} -dc oneplus3"

WORK_PATH = "/Users/amitseal/workspaces/apks/"

GPLAYCLI = WORK_PATH+"venv/bin/gplaycli"
GPLAYCLI_CONF = WORK_PATH+"gplaycli.conf"
APK_LIST = WORK_PATH+"apk_list_fake.txt"
INDEX_OUTPUT = WORK_PATH+"index_checked"
LOG_FILE = WORK_PATH+"LOG"+datetime.now().strftime('_%H_%M_%d_%m_%Y')+".txt"

OUTPUT_CSV_HEADER = "Index,ID,Processed,Downloaded,Multidex,SHA1"

RANDOM_DELAY = (3, 4)
# RANDOM_DELAY = (1, 2)


def hasher(path_apk: str):
    BLOCK_SIZE = 65536
    file_hasher = hashlib.sha1()
    with open(path_apk, 'rb') as file:
        fb = file.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hasher.update(fb)
            fb = file.read(BLOCK_SIZE)
    return file_hasher.hexdigest()


# def update_index(processed_index: int):
#     global INDEX_OUTPUT
#     with open(INDEX_OUTPUT, "w") as file:
#         file.write(str(processed_index))


def reset_log_file():
    global APK_LIST
    global LOG_FILE
    print("resetting LOG FILE")
    with open(APK_LIST) as apk_file:
        lines = apk_file.readlines()
        content = []
        for i in range(0, len(lines)):
            apk_id = get_apk_id(lines[i])
            content.append("{},{},{},{},{},{}\n".format(
                i, apk_id, False, False, False, 0))
        apk_file.close()
    with open(LOG_FILE, "w") as log_file:
        log_file.writelines(content)
        log_file.close()


def create_log_file():
    global APK_LIST
    global LOG_FILE
    apk_list_size = 0
    with open(APK_LIST) as apk_file:
        apk_list_size = len(apk_file.readlines())
    log_file_size = 0
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as log_file:
            log_file_size = len(log_file.readlines())
        if log_file_size == apk_list_size:
            print("not creating log file again")
            log_file.close()
            return
        else:
            reset_log_file()
            return
    else:
        reset_log_file()


def check_if_chosen_exists(apk_path: str):
    return os.path.exists(apk_path)


def get_apk_id(line: str):
    return line.split("_")[0]


def update_log(index_apk: int,
               apk_id: str,
               processed: bool,
               downloaded: bool,
               multidex: bool,
               sha1: str,
               log_path: str):
    contents: List[str] = []
    with open(log_path, "r") as log_file:
        contents = log_file.readlines()
    line = "{},{},{},{},{},{}".format(index_apk,
                                      apk_id,
                                      processed,
                                      downloaded,
                                      multidex,
                                      sha1)
    contents[index_apk] = line.strip()+"\n"
    print(line)
    with open(log_path, "w") as log_file:
        log_file.writelines(contents)
        log_file.close()


def count_current_number_of_apks():
    count = 0
    for entry in os.scandir('.'):
        if entry.is_file():
            name: str = entry.name
            if name.endswith(".apk"):
                count += 1
    return count


def str_to_bool(value: str) -> bool:
    if value == "True":
        return True
    else:
        return False


def split_line(line: str):
    index, apk_name, processed, downloaded, multidex, sha1 =\
        line.split(",")
    processed_bl = str_to_bool(processed)
    downloaded_bl = str_to_bool(downloaded)
    multidex_bl = str_to_bool(multidex)
    return index, apk_name, processed_bl, downloaded_bl, multidex_bl, sha1


def download():
    global COMMAND
    global GPLAYCLI
    global GPLAYCLI_CONF
    global RANDOM_DELAY
    global APK_LIST
    global WORK_PATH
    global LOG_FILE
    create_log_file()
    lines = []
    with open(LOG_FILE) as file:
        lines = file.readlines()
        file.close()
    for i in range(0, len(lines)-1):
        index: int = 0
        apk_name: str = ""
        processed: bool = False
        downloaded: bool = False
        multidex: bool = False
        sha1: str = ""
        # while count_current_number_of_apks() < limit:
        index, apk_name, processed, downloaded, multidex, sha1 = \
            split_line(lines[i])
        apk_path = WORK_PATH+apk_name+".apk"
        if(processed):
            # and check_if_chosen_exists(apk_path):
            print("{} is already processed. skipping.".format(apk_name))
            continue
        if check_if_chosen_exists(apk_path):
            print(apk_path + " already exists, skipping download.")   
        else:
            delay = random.randint(RANDOM_DELAY[0], RANDOM_DELAY[1])
            print(apk_path + " does not exist. Attempting download.")
            print("delaying for: {} seconds".format(delay))
            time.sleep(delay)
            exec_command = COMMAND.format(GPLAYCLI, apk_name, GPLAYCLI_CONF)
            exec_command = shlex.split(exec_command)
            print(exec_command)
            # subprocess.check_output(exec_command)
        processed = True
        if check_if_chosen_exists(apk_path):
            downloaded = True
            multidex = mdex.is_multidex(apk_path)
            sha1 = hasher(apk_path)
        update_log(i, apk_name, True, downloaded, multidex, sha1, LOG_FILE)
        if downloaded:
            print("removing "+apk_path)
            # os.remove(apk_path)
    print("finished downloading {} apks!".format(
        count_current_number_of_apks()))


if __name__ == "__main__":
    download()
