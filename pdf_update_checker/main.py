from __future__ import annotations
from typing import List
from bs4 import BeautifulSoup

import requests


class PDF_Update:
    def __init__(self, url: str, base_url: str, output_file: str):
        self.base_url: str = base_url
        self.web_urls: List[str] = []
        self.urls: List[str] = []
        self.content: str
        self.output_file: str = output_file

    # def read_web(self) -> PDF_Update:
    #     self.get_content_web()
    #     return self

    def read_file(self):
        self.urls = self.get_content(self.output_file).split("\n")
        return self

    def url_id(self, url: str, pattern_start: str, pattern_end: str) -> str:
        return url.split(pattern_start)[1].split(pattern_end)[0]

    def write(self):
        with open(self.output_file, "w") as file:
            for url in self.urls:
                file.write(url+"\n")
            file.close()
        return self

    def write_web(self):
        with open(self.output_file, "w") as file:
            for url in self.web_urls:
                file.write(url+"\n")
            file.close()
        self.urls = self.web_urls
        return self

    def get_content(self, file_name: str) -> str:
        with open(file_name) as file:
            content = file.read()
            file.close()
        self.content = content
        return content

    def get_content_web(self) -> PDF_Update:
        # url = "https://www.cl.cam.ac.uk/~rja14/book.html"
        # page = requests.get(self.url)
        # if page.status_code != 200:
        #     raise Exception("Oops. URL threw non 200 code.")
        # soup = BeautifulSoup(page.text, 'html.parser')
        soup = BeautifulSoup(self.get_content('source.txt'), 'html.parser')
        urls = []
        for link in soup.find_all('a'):
            current_url: str = link.get('href')
            if current_url.casefold().endswith('.pdf'):
                urls.append(self.base_url + current_url)
        self.web_urls = urls
        return self

    def filter(self, filter: str) -> PDF_Update:
        filter_urls: List[str] = []
        for url in self.urls:
            if filter.casefold() in url.casefold():
                filter_urls.append(url)
        self.urls = filter_urls
        filter_urls = []
        if len(self.web_urls) == 0: 
            self.get_content_web()
        for url in self.web_urls:
            if filter.casefold() in url.casefold():
                filter_urls.append(url)
        self.web_urls = filter_urls
        return self

    def __str__(self):
        return "\n".join(self.urls)

    def prompt_yn(self, msg: str):
        msg += "? Enter y or n: "
        if input(msg) == "y":
            return True
        else:
            return False

    def compare_urls_with_web(self, filter: str):
        self.get_content_web()
        self.filter(filter)
        if not len(self.web_urls) == len(self.urls):
            if self.prompt_yn("url count mismatch: update local"):
                self.urls = self.web_urls
                self.write()
            return self
        for i in range(0, len(self.urls)):
            if not self.urls[i] == self.web_urls[i]: 
                if self.prompt_yn("url mismatch: update local"):
                    print("Web url: "+self.web_urls[i])
                    print("Local url: "+self.urls[i])
                    self.urls[i] = self.web_urls[i]
        self.write()
        return self


if __name__ == "__main__":
    url = "https://www.cl.cam.ac.uk/~rja14/book.html"
    base_url = "https://www.cl.cam.ac.uk/~rja14/"
    pdfs = PDF_Update(
        url, base_url, "url.txt").read_file().filter(
            "SEv3")
    pdfs.compare_urls_with_web("SEv3")
    # pdfs.compare_urls_with_web("SEv3")

    # print(pdfs)
    # print(pdfs.url_id(pdfs.urls[10], "-ch", "-"))

    # print(get_content())
