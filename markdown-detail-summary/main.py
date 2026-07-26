import argparse
import re
from typing import List
from enum import Enum
import random


classes_used = 0

class LineType(Enum):
    TEXT = 1
    HEADER = 2
    ITEM = 3

all_class_names = [
    "dangerm",
    "errorm",
    "hintm",
    "tipm",
    "notem",
    "seealsom",
    "todom"]


Classes = {}


def reset_classes():
    global Classes
    global classes_used
    classes_used = 0
    for i in range(0,len(all_class_names)):
        Classes[i] = (all_class_names[i], False)

def class_supplier():
    global Classes
    global classes_used
    random_int = 0
    if classes_used == len(all_class_names)-1:
        reset_classes()
    while True:
        random_int = random.randint(0, len(Classes.keys())-1)
        if Classes[random_int][1]:
            continue
        else:
            Classes[random_int] = (Classes[random_int][0], True)
            classes_used += 1
            return Classes[random_int][0]

def read_file(file_path:str):
    lines = []
    with open(file_path) as file:
        lines = file.readlines()
    return lines

def find_indent_spaces(line:str):
    return len(line) - len(line.lstrip())

def line_type(line:str) ->LineType:
    if line.strip().startswith("#"):
        return LineType.HEADER
    if line.strip().startswith("-"):
        return LineType.ITEM
    else:
        return LineType.TEXT

def process_item(current_line: str, lines: str, current_index: int):
    length = len(lines)
    if length < 2:
        return current_line
    splitted = current_line.lstrip().split(" ", maxsplit=1)
    content = splitted[0].replace("-","") + " "+splitted[1]
    content = content.strip()
    next_index = current_index + 1
    next_line_indent_level = 0
    current_line_indent_level = 0
    if next_index < length:
        next_line:str = lines[next_index]
        current_line_indent_level = find_indent_spaces(current_line)
        next_line_indent_level = find_indent_spaces(next_line)
    if next_line_indent_level > current_line_indent_level:
        return "<details class = '{}'>\n<summary>".format(class_supplier())+content+"</summary>"

    else:
        return content

def is_continuous(line: str, previous_line:str) -> bool:
    if len(previous_line.strip()) == 0:
        return False
    else:
        return True


def process_header(line_header: str, is_this_first_header_seen: bool = False):
    content = line_header.replace("#", "").strip()
    if is_this_first_header_seen:
        return "\n<details class = '{}'>\n<summary>".format(class_supplier())+content+"</summary>"
    else:
        return "</details>"+\
            "\n<details class = '{}'>\n<summary>".format(class_supplier())+content+"</summary>"


def process_lines(lines: List[str]):
    new_lines = []
    current_indent = 0
    previous_indent = 0
    heading_first: bool = False
    current_line_type: LineType = LineType.TEXT
    previous_line_type: LineType = LineType.TEXT
    current_line:str = ""
    is_this_first_header_seen: bool = True
    is_processing_item = False
    is_processing_header = False
    length = len(lines)
    for i in range(0, len(lines)):
        current_line = lines[i]
        if len(current_line.strip()) < 1:
            if is_processing_item:
                is_processing_item = False
                new_lines.append("</details>")
            new_lines.append(current_line)
            continue
        if line_type(current_line) == LineType.HEADER:
            is_processing_header = True
            new_lines.append(process_header(current_line, is_this_first_header_seen))
            is_this_first_header_seen = False
        elif line_type(current_line) == LineType.ITEM:
            new_lines.append(process_item(current_line, lines, i))
            is_processing_item = True
        else:
            new_lines.append(current_line.strip())
    new_lines.append("</details>")
    return new_lines

def write_file(lines: List[str], filename):
    with open(filename, "w") as file:
        for line in lines:
            file.write(line+"\n")

reset_classes()

write_file(
    process_lines(
        read_file("source.md")), "output.html")