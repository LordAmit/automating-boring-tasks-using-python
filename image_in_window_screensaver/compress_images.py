import os.path
import shlex
import argument_handler as argh
import file_walker as walker
from typing import List
import os.path as path
import subprocess

def compress_image(old_image_path, new_image_path):
    command = "convert -quality 95 '{old}' '{new}'".format(
        old=old_image_path,
        new=new_image_path)
    print(command)
    subprocess.check_output(shlex.split(command))


def backup_image(old_image_path, backup_path):
    print("Backing up images")
    command = "mv '{old}' '{backup_path}'".format(old=old_image_path,
                                                  backup_path=backup_path)
    print(command)
    subprocess.check_output(shlex.split(command))


# def compress_first_10_images():


if __name__ == '__main__':
    hard_limit = 5491520
    # 5491520 bytes = 5240 KB = 5MB
    backup_path = argh.get_backup()
    image_paths: List = walker.walk(increasing_size_sort=True)
    new_suffix = "_comp_la"
    new_ext = '.jpg'
    for image_path in image_paths:
        if new_suffix in image_path:
            continue
        if os.path.getsize(image_path) < hard_limit:
            print(image_path)
            print("image size > hard limit; stopping")
            break
        old_image_path: str = image_path
        new_image_path = old_image_path.replace(
            os.path.splitext(old_image_path)[1], new_suffix + new_ext)
        compress_image(old_image_path, new_image_path)
        backup_image(old_image_path, backup_path)

        # break
        # print(image_path)
        # image_1, image_2 = os.path.split(image_path)
        # print(image_1, image_2)
        # print(os.path.splitext(image_path))
        # print(os.path.split)
        # break
