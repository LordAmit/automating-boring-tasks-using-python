from os import path as Path
from typing import List
import custom_log as l
import os
import argument_handler as argh


def walk() -> List:
    """
    walks through a path to return list of absolute path of images with png or jpg extensions
    :param path: to the directory where images will be searched for
    :return: List of string path of images
    """
    file_paths = []
    path: str = argh.get_path()
    l.log(path)
    keyword: str = argh.get_keyword()
    extension: str = argh.get_extension()
    l.log("checking path integrity")
    if Path.exists(path):
        l.log([path, "exists"])
    else:
        l.log("path does not exist")
        exit()
    for folderName, subfolders, filenames in os.walk(path):
        for filename in filenames:
            if extension:
                l.log("checking fot extension: "+extension)
                l.log("with filename: "+filename)
                if filename.endswith(extension):
                    l.log("extension matched")
                    file_path = os.path.join(folderName, filename)
                else:
                    continue
            else:
                file_path = os.path.join(folderName, filename)

            l.log([file_path, filename])

            file_paths.append(file_path)
    return file_paths
