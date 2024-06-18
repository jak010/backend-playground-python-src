from __future__ import annotations

from datetime import datetime

from bs4 import BeautifulSoup, element

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter


class InitContentTagFilter(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        soup = BeautifulSoup(self.html_source, "html.parser") \
            .find("section", {"class": "Main-content"})
        return soup


class ExtractContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        data = dict(
            title="",
            reference_date="",
            content="",
            thumbnail=""
        )

        data["title"] = html_element.find("h1", {"class": "BlogItem-title"}).text

        data["reference_date"] = html_element.find("time", {"class": "Blog-meta-item Blog-meta-item--date"},
                                                   datetime=True).get("datetime")

        thumbnail_tag = html_element.find("div", {"class": "image-block-wrapper"})
        if thumbnail_tag:
            data["thumbnail"] = thumbnail_tag.find("img").get("data-src")

        content_list = []
        contents = html_element.find_all("div", {"class": "sqs-block-content"})
        for content in contents:
            if content.find("div", {"class": "sqs-html-content"}):
                p_tag = content.find_all('p', {"style": "white-space:pre-wrap;"})
                for p in p_tag:
                    content_list.append(p.text)
            if content.find("div", {"class": "image-block-wrapper"}):
                img_tag = content.find('img')
                content_list.append(img_tag.get("data-src"))
            if content.find("blockquote"):
                sns = [a_tag for a_tag in content.find_all('a') if a_tag.get('href')]
                content_list.append(sns[-1].get('href'))

        data["content"] = "\n".join(content_list)

        return data
