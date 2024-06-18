from __future__ import annotations

import bs4.element
from bs4 import BeautifulSoup

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter


class InitContentTagFilterAbstract(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        return BeautifulSoup(self.html_source, "html.parser")


class SelectElementTagFilter(AbstractScrapFilter):

    def execute(self, html_element):
        # page 1 ~ 23
        phase1 = html_element.find("div", {"class": ["wp-container-62 wp-block-query"]})

        # page 23
        phase2 = html_element.find("div", {"class": ["wp-container-54 wp-block-query"]})

        return phase1 or phase2


class ExtractContentTagFilter(AbstractScrapFilter):
    def execute(self, html_element):
        element_tag = []

        phase1 = html_element.find(
            "ul", {
                "class": [
                    "wp-container-59 is-flex-container columns-3 home-block-style block-list three-blocks wp-block-post-template"]
            })

        phase2 = html_element.find(
            "ul", {
                "class": [
                    "wp-container-51 is-flex-container columns-3 home-block-style block-list three-blocks wp-block-post-template"
                ]
            })

        tags = phase1 or phase2

        for tag in tags:
            element_tag.append(tag.find("figure").find("a")["href"])

        return element_tag
