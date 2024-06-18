from __future__ import annotations

import bs4

from src.adapter.abstract.abstract_pipe import AbstractScrapFilter
from bs4 import BeautifulSoup, element


class InitContentTagFilter(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        soup = BeautifulSoup(self.html_source, "html.parser") \
            .find("div", {"id": "baza"})
        return soup


class SelectContentTagFilter(AbstractScrapFilter):

    def execute(self, html_source):
        return html_source.find("div", {"id": "wrap"}).find("div", {"id": "contents"})


class ExtractContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        data = {
            "reference_date": "",
            "title": "",
            "content": "",
            "imgs": []
        }

        article = html_element.find("div", {"class": "article_wrap"})
        article_tags = [tag for tag in article if isinstance(tag, bs4.element.Tag)]

        for article_tag in article_tags:
            if title := self._extract_title(article_tag):
                data['title'] = title.text
            if reference_date := self._extract_reference_date(article_tag):
                data['reference_date'] = reference_date.text.strip()

        contents_tags = [tag for tag in html_element.find("div", {"class": "atc_content"})
                         if isinstance(tag, bs4.element.Tag)]
        for contents_tag in contents_tags:
            current_img = ""
            if contents_tag.attrs == {'class': ['ab_photo', 'photo_center']}:
                if img := contents_tag.find('img'):
                    current_img = img.get('lazy')
                    data['imgs'].append(current_img)
                if img := contents_tag.find("div", {"class": "image"}):
                    current_img = img.find("img").get('src')
                    data['imgs'].append(current_img)

            if contents_tag.attrs == {'class': ['tag_photobundle']}:
                if img := contents_tag.find('img'):
                    current_img = img['lazy']
                    data['imgs'].append(current_img)
            if contents_tag_vod := contents_tag.find("div", {"class": "tag_vod"}):
                current_img = contents_tag_vod['data-id']
                data['imgs'].append(current_img)
            if imgs := contents_tag.findAll("img"):
                for img in imgs:
                    if img_src := img.get('lazy'):
                        current_img = img_src
                        data['imgs'].append(current_img)
            if contents_tag_vod := contents_tag.find("div", {"class": "tag_sns"}):
                current_img = contents_tag_vod['data-url'] + "embed/captioned/"
                data['imgs'].append(current_img)

            if contents_tag.text:
                if self.is_nonbreak(tag=contents_tag):
                    continue
                else:
                    data['content'] += current_img
                    data['content'] += contents_tag.text
            data['content'] += "\n"
        data['imgs'] = [item for item in data['imgs'] if item]
        return data

    def _extract_title(self, tag: bs4.element.Tag):
        return tag.find("h2", {"class": "tit_article"})

    def _extract_reference_date(self, tag: bs4.element.Tag):
        return tag.find("span", {"class": "time"})

    def is_nonbreak(self, tag):
        return (tag.text.encode() == b'   \xc2\xa0  ') or (tag.text.encode() == b'   \xc2\xa0  ')
