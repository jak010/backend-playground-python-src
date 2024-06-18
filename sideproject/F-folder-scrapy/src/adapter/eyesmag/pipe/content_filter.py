from __future__ import annotations

from bs4 import BeautifulSoup
import json
from src.adapter.abstract.abstract_pipe import AbstractScrapFilter


class InitContentTagFilterAbstract(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        return BeautifulSoup(self.html_source, "html.parser") \
            .find("script", {"id": "__NEXT_DATA__"})


class SelectContentFilter(AbstractScrapFilter):

    def execute(self, html_element):
        return json.loads(html_element.text).get("props", None) \
            .get("pageProps", None) \
            .get("post", None)


class ExcludeContentFilter(AbstractScrapFilter):
    def execute(self, html_json):
        import copy
        html_json = copy.deepcopy(html_json)
        html_json.pop("users.user_id")
        html_json.pop("users.user_name")
        html_json.pop("users.user_email")
        html_json.pop("users.user_url")
        html_json.pop("users.display_name")
        html_json.pop("termRelationships.term_taxonomy_id", None)
        html_json.pop("termRelationships.object_id", None)

        return html_json


class ExtractContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element):
        return html_element
