import time
import random
import subprocess
import shlex
import os

# COMMAND = "gplaycli -d {} -c gplaycli.conf"
COMMAND = "{} -d {} -c {} -dc oneplus3"
GPLAYCLI = "/Users/amitseal/workspaces/apks/venv/bin/gplaycli"
GPLAYCLI_CONF = "/Users/amitseal/workspaces/apks/gplaycli.conf"
RANDOM_DELAY = (5, 10)
# RANDOM_DELAY = (1, 2)

APK_LIST = 'apk_list.txt'


def check_if_chosen_exists(apk_name: str):
    return os.path.exists(apk_name+".apk")


def get_apk_id(line: str):
    splitted = line.split("_")
    # pre, post = splitted[0], splitted[1]
    return splitted[0]


def choose_random_from_list(lines_apk: str):
    while True:
        random_index = random.randint(0, len(lines_apk)-1)
        apk_line = lines_apk[random_index]
        apk_id = get_apk_id(apk_line)
        if check_if_chosen_exists(apk_id):
            print("chose {}, but already downloaded; skipping".format(apk_id))
            continue
        else:
            return apk_id


def count_current_number_of_apks():
    count = 0
    for entry in os.scandir('.'):
        if entry.is_file():
            name: str = entry.name
            if name.endswith(".apk"):
                count += 1
    return count


def download(limit=10):
    global COMMAND
    global GPLAYCLI
    global GPLAYCLI_CONF
    global RANDOM_DELAY
    global APK_LIST
    with open(APK_LIST) as file:
        lines = file.readlines()
        
        # if limit == 0:
        #     upper = len(lines)
        # else:
        #     upper = offset+limit
        # print("finding from {}, {}".format(offset, upper))
        # for i in range(offset, upper):
        while count_current_number_of_apks() < limit:
            print("{}/{} downloaded".format(
                count_current_number_of_apks(), limit))
            # line = lines[i]
            apk_name: str = choose_random_from_list(lines)
            delay = random.randint(RANDOM_DELAY[0], RANDOM_DELAY[1])
            print("delaying for: {} seconds".format(delay))
            time.sleep(delay)
            exec_command = COMMAND.format(GPLAYCLI, apk_name, GPLAYCLI_CONF)
            exec_command = shlex.split(exec_command)
            print(exec_command)
            subprocess.check_output(exec_command)
    print("finished downloading {} apks!".format(
        count_current_number_of_apks()))


if __name__ == "__main__":
    TO_DOWNLOAD = 100
    download(TO_DOWNLOAD)
