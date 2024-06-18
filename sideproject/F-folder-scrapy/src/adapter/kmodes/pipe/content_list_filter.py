from __future__ import annotations

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter
from bs4 import BeautifulSoup, element


class InitContentTagFilter(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        return BeautifulSoup(self.html_source, "html.parser")


class SelecContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        return html_element.find("div", {"class": "blog2_albumlist"})


class ExtractContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        data = []

        for each in html_element.findAll('a', {"class": "link pcol2"}, href=True):
            fqdn = "https://blog.naver.com" + each["href"]
            data.append(fqdn)

        return data
