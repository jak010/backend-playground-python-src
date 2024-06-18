from typing import List

from src.app.abstarct import AbstractLoaderDataType
from src.app.remaker.command_query import RemakerQuery


class RemakerExtractor:

    def __init__(self):
        self.query = RemakerQuery()

    def get_before_remake(self) -> List[AbstractLoaderDataType]:
        """ 아직 변환이 완료되지 않은 데이터 가져오기 """
        return self.query.get_by_remake(is_remake=False)
