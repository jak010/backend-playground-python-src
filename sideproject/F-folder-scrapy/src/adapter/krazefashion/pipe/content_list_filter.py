from __future__ import annotations

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter
from bs4 import BeautifulSoup, element


class InitContentTagFilter(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        soup = BeautifulSoup(self.html_source, "html.parser") \
            .find("div", {"class": "summary-item-list"})
        return soup


class ExtractContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        data = []

        links = html_element.find_all("div", {"class": "summary-title"})

        for each in links:
            link = each.find('a', {"class": "summary-title-link"}, href=True)["href"]
            data.append(link)

        return data
