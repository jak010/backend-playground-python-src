from __future__ import annotations

import bs4

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter
from bs4 import BeautifulSoup, element


class InitContentTagFilter(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        soup = BeautifulSoup(self.html_source, "html.parser") \
            .find("div", {"class": "cont_wrap"})
        return soup


class SelecContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        return html_element.find("ul", {"class": "gallery_list"})


class ExtractContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        data = []

        for each in html_element.findAll('a', href=True):
            fqdn = "https://www.fi.co.kr" + "/main/" + each["href"]
            data.append(fqdn)

        return data
