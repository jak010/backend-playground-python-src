from __future__ import annotations

from datetime import datetime

from bs4 import BeautifulSoup, element

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter


class InitContentTagFilter(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        soup = BeautifulSoup(self.html_source, "html.parser") \
            .find("div", {"class": "se-viewer se-theme-default"})
        return soup


class ExtractContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        title = html_element.find("span", {"class": "se-fs- se-ff-"}).text

        date_string = html_element.find("span", {"class": "se_publishDate pcol2"}).text

        reference_date = html_element.find("span", {"class": "se_publishDate pcol2"}).text

        img_element = html_element.find("img", {"class": "se-image-resource"})
        thumbnail = img_element.get("data-lazy-src") or img_element.get("src")

        for tag in html_element.find_all("span", {"class": "__se-hash-tag"}):
            tag.decompose()

        p_tags = html_element.find_all("p", {"class": "se-text-paragraph"})
        content = ''.join(i.text for i in p_tags if i.text != '\u200b')

        return {
            "title": title,
            "reference_date": reference_date,
            "thumbnail": thumbnail,
            "content": content
        }
