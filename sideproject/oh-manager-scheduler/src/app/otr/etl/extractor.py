from typing import List

import requests
from bs4 import BeautifulSoup


class OTRClient:

    def __init__(self):
        self.base_url = "https://otr.co.kr/audition/?"

    def get_board_contents(self, category: str, board_page: int):
        resp = requests.get(self.base_url, params={
            "board_name": "audition",

            "board_page": board_page,
            "mode": "list",
            "category1": category,
            "list_type": "list",
            "lang": "ko_KR"
        })
        if resp.status_code == 200:
            return resp.text


class OTRExtractor:

    def __init__(self):
        self.client = OTRClient()

    def get_moive_pages(self, board_page: int) -> List[str]:
        page = self.client.get_board_contents(category="영화", board_page=board_page)

        return self._get_board_page_urls(page=page)

    def _get_board_page_urls(self, page):
        """ 게시판에에 존재하는 urls 반환 """
        result = []
        soup = BeautifulSoup(page, "html.parser")

        board = soup.find("tbody", {"id": "audition_board_body"})
        for row in board.findAll("tr"):
            href_link = row.find("a").get("href")
            href_link = href_link.replace("amp", "")
            result.append(href_link)

        return result
