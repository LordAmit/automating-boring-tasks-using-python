#!/bin/python3

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


if __name__ == '__main__':
    import folder_walk as walk
    import argument_handler as argh
    from typing import List

    l.disable()

    keyword = argh.get_keyword()
    l.log("started parsing directories")
    file_paths: List[str] = walk.walk()
    l.log("will start scanning files now.")
    all_rules = rule_builder.get_rules()

    for file_path in file_paths:
        count_issues: int = 0
        print("at file: " + file_path)
        lines: List[str] = open(file_path).readlines()
        for line in lines:
            if will_i_process_line(line):
                line_issues = line_checker.check_line(line, all_rules)
                count_issues += line_issues
        print("done with: " + file_path)
        print("total issues found: " + str(count_issues))
