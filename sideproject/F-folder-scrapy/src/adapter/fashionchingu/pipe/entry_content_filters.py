from __future__ import annotations

from bs4 import BeautifulSoup, element

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter


class InitContentTagFilterAbstractScrapFilter(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        return BeautifulSoup(self.html_source, "html.parser").find("main", {"id": "site-content"})


class SelectElementTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        return html_element.find("div", {"class": "main_section single_post"})


class ExtractContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        data = {
            'title': '',
            'reference_date': '',
            'content': '',
            'imgs': []
        }
        content_tags = html_element.find("div", {"class": "row"})

        title = content_tags.find("h1").text
        reference_date = content_tags.find("p", {"class": "date_published"}).text

        data['title'] = title
        data['reference_date'] = reference_date
        for content_tag in content_tags:
            data['content'] += content_tag.text

        for img in content_tags.find_all("div", {"class": "wp-block-image"}):
            if img_src := img.find("img").get("data-lazy-src"):
                data['imgs'].append(img_src)

        if not data['imgs']:
            for img in content_tags.find_all('img'):
                data['imgs'].append(img.get("data-lazy-src"))

        return data
