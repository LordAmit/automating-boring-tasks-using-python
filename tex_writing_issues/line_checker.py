import custom_log as l
from typing import List
import re


def _print_red(value: str):
    print("\033[91m {}\033[00m".format(value))


def check_line(line: str, rules_packs: List):
    count_issues: int = 0
    line = line.lower().strip()
    for rule_pack in rules_packs:
        rule_name = rule_pack[0]
        rules = rule_pack[1]
        l.log("rule_name: " + rule_name)
        for rule in rules:
            keyword = rule[0]
            l.log("keyword: " + keyword)
            regex = re.compile(r"\b{}\b".format(keyword))
            if len(regex.findall(line)) != 0:
                print("""
                issue: {}, issue type: {},  
                line: {}
                replace with: {}""".format(keyword, rule_name, line, rule[1:]))
                count_issues += 1
    return count_issues
