#!/usr/bin/env python3
import time
import random
import re

# https://github.com/search?p=4&q=Cipher.getInstance&type=Code

class IterSearch():
    def __init__(self) -> None:
        
        self.matched_urls: list[str] = []
        self.url_search: str = "https://github.com/search?p=P@#&q=Cipher.getInstance&type=Code"
        self.token_iter: str = "P@#"
        self.iter_start: int = 4
        self.iter_end: int = 10
        self.token_keyword: str = None
        self.expressions
        self.pause_seconds: int = None
        self.random_delay: list[int] = (5, 10)

    # "Cipher\.getInstance\(\"[A-Z]+\"\)"
    def add_expression(self, expression):
        self.expressions.add(expression)

    def _append_matched_url(self, URL: str):
        self.matched_urls.append(URL) 

    def _adding_pause(self):
        delay = random.randint(self.random_delay[0], self.random_delay[1])
        time.sleep(delay)

    def iter_url(self):
        # including the iter_end itself
        for i in range(self.iter_start, self.iter_end+1):
            self._adding_pause()
            formatted_URL: str = self.url_search.replace(
                self.token_iter, 
                str(i)
                ).replace(
                    self.token_keyword, 
                    self.keyword)
            content = self._get_content_from_url(formatted_URL)
            if self._find_word_in_content(content, self.keyword):
                self._append_matched_url(formatted_URL)

    def _get_content_from_url(self, URL: str) -> str:
        return None
    
    def _find_expression_in_content(self, content: str):
        for expression in self.expressions:
            return re.findall(pattern, content)


if __name__ == "__main__":
    pass