from __future__ import annotations

import bs4.element
from bs4 import BeautifulSoup

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter


class InitContentTagFilter(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        return BeautifulSoup(self.html_source, "html.parser")


class SelectElementTagFilter(AbstractScrapFilter):

    def execute(self, html_element):
        return html_element.find("div", {"class": "wp-site-blocks"})


class ExtractContentTagFilter(AbstractScrapFilter):
    def execute(self, html_element):

        data = {
            "title": "",
            "reference_date": "",
            "thumbnail": "",
            "content": ""
        }

        for e in html_element:

            if isinstance(e, bs4.element.Tag):
                if title := e.find("h1", {
                    'style': 'margin-bottom: 0px; margin-top: 0px; margin-right: 0px; margin-left: 0px;',
                    'class': ['has-text-align-center', 'alignwide', 'ys-post-title', 'wp-block-post-title',
                              'has-source-serif-pro-font-family']}):
                    data["title"] = title.text
                if date_published := e.find("div", {"class": "wp-block-post-date"}):
                    data['reference_date'] = date_published.find("time")['datetime']
                if thumbnail := e.find("figure", {
                    "class": ["ys-post-featured-image wp-block-post-featured-image"]}):
                    data['thumbnail'] = thumbnail.find("img")["src"]

                # content
                for each in e.findAll("div"):
                    if each.attrs.get("class", None) and "entry-content" in each.attrs.get("class", None):
                        data['content'] += each.text

                        if img := each.find("img"):
                            data['content'] += img['src']

        return data
