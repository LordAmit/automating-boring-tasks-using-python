import custom_log as l
import os
from typing import List


def get_rules() -> List:
    all_rules = _build_rules(["ambiguous", "complicated", "offensive", "strong"])
    l.log("rules found are: " + str(all_rules))
    return all_rules


def _build_rules(rule_names: List) -> List:
    path_rules = "/home/amit/git/automating-boring-tasks-using-python/tex_writing_issues/"
    all_rules: List = []
    for rule_name in rule_names:
        l.log("working with rule: " + rule_name)
        f_rule = path_rules + "words_" + rule_name
        l.log("rule file name: " + f_rule)
        current_rules: List = []
        if not os.path.exists(f_rule):
            l.log("file_rule {} NOT FOUND. EXITING".format(f_rule))
            exit()

        l.log("path to rule: " + f_rule)
        rules: List[str] = open(f_rule).readlines()
        for rule in rules:
            rule_key = rule.split(',')[:1][0].strip().lower()
            rule_value = _clean_rule(rule.split(',')[1:])
            # double parenthesis, because we are adding a tuple in append function
            current_rules.append(
                (rule_key, rule_value)
            )
        # again, double parenthesis, because we are adding a tuple in append function
        all_rules.append((rule_name, current_rules))
    return all_rules


def _clean_rule(rules: List[str]) -> List[str]:
    cleaned_rules: List[str] = []
    for rule in rules:
        current_rule: str = rule
        current_rule = current_rule.strip().lower()
        cleaned_rules.append(current_rule)
    return cleaned_rules
