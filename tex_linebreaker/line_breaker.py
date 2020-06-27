#!/usr/bin/env python3
# 
# Adds new line in between sentences separated by periods. Respects existing line breaks, tries to respect indentation.


from typing import List
import os
import shutil
import argparse


class LineBreaker:

    def file_to_file_compare(self, file_path1: str, file_path2: str):
        content1 = None
        content2 = None
        with open(file_path1) as f1:
            content1 = f1.readlines()
        with open(file_path2) as f2:
            content2 = f2.readlines()
        
        content1 = "\n".join(content1)
        content2 = "\n".join(content2)
        
        serial1 = []
        serial2 = []
        for ch in content1:
            if not ch.isspace():
                serial1.append(ch)
        for ch in content2:
            if not ch.isspace():
                serial2.append(ch)
        print(str(len(serial1)), str(len(serial2)))
        
    def __init__(self, file_path):

        if os.path.exists(file_path):
            self.original_path = file_path
            filename = os.path.splitext(file_path)[0]
            self.backup_path = filename+".backup"+".tex"
            self.new_contents: List[str] = []
            if os.path.exists(self.backup_path):
                print("ERROR: Must delete backup file before proceeding.")
                exit(-1)
            shutil.copyfile(self.original_path, self.backup_path)
            with open(file_path, "r") as reader:
                self.contents: List[str] = reader.readlines()
                if len(self.contents) < 0:
                    raise ValueError("File has no content")
                
            self.__process_lines()
            with open(file_path, "w") as writer:
                writer.writelines(self.new_contents)

            self.file_to_file_compare(self.backup_path, self.original_path)
        else:
            raise FileNotFoundError

    def __period_handling(self, line: str) -> str:
        # range is shortened, so that we can skip the last period
        current_line = ""
        for i in range(0, len(line)):
            current_line += line[i]
            if line[i] == ".":
                # check if . has alphanumeric at left, and space at right
                if i+1 != len(line):
                    if line[i+1].isspace():
                        # introduce linebreak at line[i+1 position]
                        current_line += "\n"
        proper_stripped_lines = current_line.splitlines()
        current_line = ""
        for line in proper_stripped_lines:
            current_line += line.lstrip() + "\n"
        return current_line.lstrip()

    def __is_comment(self, line: str) -> bool:
        return line.startswith("%")

    def __copy_whitespace(self, old_line: str, processed_line: str):
        prefix_whitespace = ""
        for character in old_line: 
            if character.isspace():
                prefix_whitespace += character
            else:
                break
        return prefix_whitespace + processed_line
        # try:
        #     prefix_whitespace + processed_line
        # except TypeError:
        #     print(prefix_whitespace, processed_line)

    def __process_lines(self):
        for line in self.contents:
            # check length, if contains too few characters, copy, continue
            if len(line) < 1:
                self.new_contents.append(line)
                continue
            #  if comment, copy it as it is
            if self.__is_comment(line):
                self.new_contents.append(line)
                continue
            # strip line
            stripped_line = line.strip()
            processed_line = self.__period_handling(stripped_line)
            processed_line = self.__copy_whitespace(line, processed_line)
            self.new_contents.append(processed_line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Process tex file to insert new line \
    after period, selectively.")
    parser.add_argument("path")
    args = parser.parse_args()
    LineBreaker(args.path)
        
