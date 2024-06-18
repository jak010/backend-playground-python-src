from urllib.parse import urlparse, parse_qs

import datetime
import requests
from bs4 import BeautifulSoup

from src.app.otr.command_query.dto import OTRAuditionDto


class OTRTransform:

    def __init__(self, url):
        self.url = url

    @property
    def query_string(self) -> dict:
        parts = urlparse(self.url)
        return parse_qs(parts.query)

    def execute(self):
        resp = requests.get(self.url)

        vid = self.query_string.get("vid", [None])[0]

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")

            audition_board = soup.find("div", {"id": "audition_board_box"})
            audition_title = audition_board.find("tr", {"id": "mb_audition_tr_title"}).findAll("span")[1].text  # 제목
            audition_contents = audition_board.find("tr", {"id": "mb_audition_tr_content"}).text.replace(u"\xa0", u"")  # 내용

            if audition_contents_attachmenet := audition_board.find("tr", {"id": "mb_audition_tr_content"}).find("img"):
                audition_contents += audition_contents_attachmenet.get("src", "")  # 본문에 이미지 파일이 첨부된 경우

            audition_category = audition_board.find("tr", {"id": "mb_audition_tr_category1"}).findAll("span")[1].text  # 카테고리
            audition_tax = audition_board.find("tr", {"id": "mb_audition_tr_ext2"}).findAll("span")[1].text  # 페이
            audition_end_date = audition_board.find("tr", {"id": "mb_audition_tr_edate"}).findAll("span")[1].text  # 마감날짜
            audition_author = audition_board.find("tr", {"id": "mb_audition_tr_user_name"}).findAll("span")[1].text  # 작성자

            dt = datetime.datetime.strptime(audition_end_date, "%Y-%m-%d")

            # 마감날짜가 유효한 것
            if dt > datetime.datetime.now():
                return OTRAuditionDto.new(
                    vid=vid,
                    title=audition_title,
                    content=audition_contents,
                    category=audition_category,
                    reward=audition_tax,
                    link=self.url,
                    end_date=audition_end_date,
                    author=audition_author
                )
