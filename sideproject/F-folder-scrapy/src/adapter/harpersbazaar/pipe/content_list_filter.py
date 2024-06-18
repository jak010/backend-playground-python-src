from __future__ import annotations

import bs4

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter
from bs4 import BeautifulSoup, element


class InitContentTagFilter(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        soup = BeautifulSoup(self.html_source, "html.parser") \
            .find_all("div", {"class": "articlebox"})
        return soup


class ExtractContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        data = []

        for each in html_element:
            if isinstance(each, bs4.Tag):
                if each := each.find("a"):
                    data.append("https://www.harpersbazaar.co.kr" + each['href'])
        return data
