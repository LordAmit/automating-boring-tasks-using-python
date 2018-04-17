import subprocess
from typing import List
import shlex

command_list_connections = "nmcli con show Hotspot"


def hotspot_exists():
    try:
        subprocess.check_output(shlex.split(
            command_list_connections)).decode().split('\n')
        return True
    except subprocess.CalledProcessError as error:
        return False


def check_hotspot_active():
    try:
        if not hotspot_exists():
            return False
        lines: List[str] = subprocess.check_output(shlex.split(
            command_list_connections)).decode().split('\n')

        for line in lines:
            if line.find("GENERAL.STATE") is not -1:
                if line.find("activated") is not -1:
                    return True
        return False
    except subprocess.CalledProcessError as error:
        return False


def status_hotspot_autoconnect():
    try:
        if not hotspot_exists():
            return -1
        lines: List[str] = subprocess.check_output(shlex.split(
            command_list_connections)).decode().split('\n')
        for line in lines:
            if line.find('connection.autoconnect') is not -1:
                if line.find('yes') is not -1:
                    return True
                else:
                    return False
        else:
            return -1
    except subprocess.CalledProcessError as error:
        return -1


def set_autoconnect(value: bool):
    if not hotspot_exists():
        return "Error"
    command = "nmcli connection modify Hotspot" +\
        " connection.autoconnect {}".format(
            str(value).upper())
    try:
        subprocess.check_output(shlex.split(command))
        return True
    except subprocess.CalledProcessError as error:
        return False


def main():
    set_autoconnect(False)


if __name__ == '__main__':
    main()
