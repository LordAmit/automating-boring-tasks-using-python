import custom_log as l
from typing import List
import re


def _print_red(value: str):
    print("\033[91m {}\033[00m".format(value))


def check_line(line: str, rules: List):
    line = line.lower().strip()
    rule_ambiguous: List = rules[0]
    rule_complicated: List = rules[1]
    rule_offensive: List = rules[2]
    rule_strong: List = rules[3]

    for rule in rule_ambiguous:
        keyword = rule[0]

        regex = re.compile(r"\b{}\b".format(keyword))
        if len(regex.findall(line)) != 0:
            print("""
            issue found: ambiguous
            line: {}
            issue: {}
            fix: {}
            """.format(line, keyword, rule[1:]))

        # l.log("no issue with " + line)
