#!/usr/bin/env python3

from PIL import Image
import sys
import os
import shutil
from typing import List


class LandPortSort:
    PORTRAIT = 1
    LANDSCAPE = 0

    def __init__(self, working_dir=os.getcwd()):
        self.cur_dir: str = working_dir+"/"
        self.landscape_dir:str = self.cur_dir+"landscape/"
        self.portrait_dir:str = self.cur_dir+"portrait/"
        self.image_list : List = []
        self.image_exts: List = ['.jpg', '.jpeg', '.png', '.bmp']

        # print(self.cur_dir)

        self.make_directories(self.landscape_dir)
        self.make_directories(self.portrait_dir)

        self.walk_dir_for_images()
        self.move_images()
        # print(self.image_list)

    def make_directories(self, dir_path):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    def walk_dir_for_images(self):
        for f in os.listdir(self.cur_dir):
            file_path = os.path.join(self.cur_dir, f)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                if ext in self.image_exts:
                    self.image_list.append(file_path)


    def move_images(self):
        for image_path in self.image_list:
            self.move_image(image_path)
        # print(files)

    def move_image(self, image_path):
        if self.process_image(image_path) is LandPortSort.PORTRAIT:
            print(image_path, self.portrait_dir)
            shutil.move(image_path, self.portrait_dir)
        else:
            print(image_path, self.landscape_dir)
            shutil.move(image_path, self.landscape_dir)


    def process_image(self, image_path: str):
        current_image: Image.Image = Image.open(image_path)
        width, height = current_image.size
        current_image.close()
        print(height, width)
        if height > width:
            return LandPortSort.PORTRAIT
        else:
            return LandPortSort.LANDSCAPE


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # print("found argument")
        # print(sys.argv)
        LandPortSort(sys.argv[1])
    else:
        LandPortSort()
