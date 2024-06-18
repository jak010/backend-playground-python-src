from __future__ import annotations

from bs4 import BeautifulSoup, element

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter

STOP_DATE = "2022"


class RaiseStopException(Exception):
    """ 2022년 데이터면 종료 """


class InitContentTagFilter(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        soup = BeautifulSoup(self.html_source, "html.parser") \
            .find("div", {"class": "detail_wrap"})
        return soup


class ExtractContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        title = html_element.find("h3", {"class": "d_title"})
        refernce_date = html_element.find("p", {"class": "d_write"}).text.split("\xa0")[0]  # NBSP로 split
        content = html_element.find("div", {"class": "d_cont"})
        imgs = []

        for elem in content.find_all("img"):
            imgs.append(elem["src"])

        if refernce_date.split("-")[0] == STOP_DATE:
            raise RaiseStopException()

        return {
            "title": title.text,
            "content": str(content) + '\n'.join(imgs),
            "reference_date": refernce_date,
            'thumbnail': imgs[0] if imgs else ""
        }
