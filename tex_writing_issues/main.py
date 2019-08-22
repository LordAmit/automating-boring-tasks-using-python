#!/usr/bin/env python3

import custom_log as l
from typing import List
import rule_builder
import line_checker


def will_i_process_line(line: str) -> bool:
    # comments checking
    if line.startswith("%"):
        return False
    else:
        return True


def process_file(file_path: str, all_rules: List):
    count_issues: int = 0
    print("at file: " + file_path)
    lines: List[str] = open(file_path).readlines()
    for line in lines:
        if will_i_process_line(line):
            line_issues = line_checker.check_line(line, all_rules)
            count_issues += line_issues
    print("done with: " + file_path)
    print("total issues found: " + str(count_issues))


if __name__ == '__main__':
    import folder_walk as walk
    import argument_handler as argh
    from typing import List

    l.disable()
    all_rules = rule_builder.get_rules()
    if argh.get_file_path() is not None:
        print("single file given : "+argh.get_file_path())
        l.log("single file input")
        process_file(argh.get_file_path(), all_rules)
    elif argh.get_dir_path() is not None:
        l.log("directory is given. scanning files from directory")
        file_paths: List[str] = walk.walk()
        for file_path in file_paths:
            process_file(file_path, all_rules)
            print()
    else:
        print("neither path nor file was declared. Run with -h switch for help")
