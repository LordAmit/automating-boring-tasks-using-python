#!/usr/bin/env python3
from typing import List
import os
import argparse


class SillyChecker:  
    def __init__(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as reader:
                self.contents: List[str] = reader.readlines()
                if len(self.contents) < 0:
                    raise ValueError("File has no content")      
            self.__process_lines()
        else:
            raise FileNotFoundError

    def __is_comment(self, line: str) -> bool:
        return line.startswith("%")

    def check_words_count(self, line: str, look_for: str, ref_word: str, reason: str = None):
        if look_for in line:
            if not line.count(look_for) == line.count(ref_word):
                    print("Check for {} issues in line: {} ".format(ref_word, line))
                    if reason:
                        print(reason)

    def __process_lines(self):
        for line in self.contents:
            if len(line) < 1 or self.__is_comment(line):
                continue
            else:
                self.check_words_count(line, "\cite{", "~\cite{", "~ before cite")
                self.check_words_count(line, "\ref{", "~\ref{", "~ before ref")
                self.check_words_count(line, ", that ", " that ", "no , before that")
                self.check_words_count(line, " which ", ", which ", "comma before which")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Process tex file to check for \
        ~ before ref, cite, and for checking that and which.")
    parser.add_argument("path")
    args = parser.parse_args()
    SillyChecker(args.path)
        
