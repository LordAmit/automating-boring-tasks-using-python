import custom_log as l
import os
from typing import List


def build_rules() -> List:
    return [_build_ambiguity(),
            _build_complicated(),
            _build_offensive(),
            _build_strong()]


def _build_ambiguity() -> List:
    file_name: str = "words_ambiguous"
    return _build_rule(file_name)


def _build_complicated() -> List:
    file_name: str = "words_complicated"
    return _build_rule(file_name)


def _build_offensive() -> List:
    file_name: str = "words_offensive"
    return _build_rule(file_name)


def _build_strong() -> List:
    file_name: str = "words_strong"
    return _build_rule(file_name)


def _build_rule(rule_file_path: str) -> List:
    current_rules: List = []
    f_rule: str = rule_file_path
    if os.path.exists(f_rule):
        l.log("path to rule: " + f_rule)
        rules: List[str] = open(f_rule).readlines()
        for rule in rules:
            rule_key = rule.split(',')[:1][0].strip().lower()
            rule_value = _clean_rule(rule.split(',')[1:])
            # double parenthesis, since we are adding a tuple in append function
            current_rules.append(
                (rule_key, rule_value)
            )
    return current_rules


def _clean_rule(rules: List[str]) -> List[str]:
    cleaned_rules: List[str] = []
    for rule in rules:
        current_rule: str = rule
        current_rule = current_rule.strip().lower()
        cleaned_rules.append(current_rule)
    return cleaned_rules
