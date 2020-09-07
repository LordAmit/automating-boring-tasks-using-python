import os
from typing import List
import argparse


def read_review_file(file_path: str) -> List[str]:
    formatted_lines: List[str] = []
    heading: bool = False
    heading_mark = "#"
    if not os.path.exists(file_path):
        raise Exception("Incorrect file path")
    with open(file_path) as file:
        lines: List[str] = file.readlines()
    for line in lines:
        if line.startswith("==-=="):
            continue
        elif line.startswith("==+=="):
            line = line.replace("==+==", heading_mark)
            if not heading:
                heading = True
                heading_mark = "##"
        formatted_lines.append(line)
    return formatted_lines


def write_file(file_path: str, lines: List[str]):
    # if os.path.exists(file_path):
    #     raise Exception("file already exists")
    with open(file_path, "w") as file:
        file.writelines(lines)


if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(description='Processes review text files\
         and spews out markdown.')
    
    parser.add_argument("input", help="full path to the input file")    
    args = parser.parse_args()

    write_file(args.input+"_formatted.md", read_review_file(args.input))

