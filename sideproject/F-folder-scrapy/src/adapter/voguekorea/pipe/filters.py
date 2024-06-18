from __future__ import annotations

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter
from bs4 import BeautifulSoup, element


class InitContentTagFilterAbstract(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        return BeautifulSoup(self.html_source, "html.parser") \
            .find("div", {"class": "contt"})


class SelectElementTagFilter(AbstractScrapFilter):

    def execute(self, html_element):
        element_tag = []
        for content in html_element:
            if isinstance(content, element.Tag):
                element_tag.append(content)
        return element_tag


class ExcludeElementTagFilter(AbstractScrapFilter):

    def execute(self, html_element):
        element_tag = []
        for elem in html_element:
            if elem.attrs.get("class") == ['relate_group', 'relate_content']:
                continue
            element_tag.append(elem)
        return element_tag


class ExtractContentTagFilter(AbstractScrapFilter):
    def execute(self, html_element):
        element_tag = []
        for elem in html_element:
            element_tag.append(str(elem))

        return element_tag
