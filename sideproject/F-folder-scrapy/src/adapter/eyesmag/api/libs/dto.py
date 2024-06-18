import dataclasses

from src.adapter.abstract.abstract_dto import AbstractDto


class EyesMagDto(AbstractDto):

    @classmethod
    def new(
            cls,
            *,
            id=None,
            trace_id=None,
            reference_id=None,
            reference_date=None,
            reference_link=None,
            title=None,
            content=None,
            thumbnail=None
    ):
        return cls(
            id=id,
            trace_id=trace_id,
            reference_id=reference_id,
            reference_date=reference_date,
            reference_link=reference_link,
            title=title,
            content=content,
            thumbnail=thumbnail
        )

    def __lt__(self, other):
        return int(self.reference_id) < int(other.reference_id)


@dataclasses.dataclass
class Post:
    ID: int
    title: str
    excerpt: str
    name: str
    publishedAt: str

    thumbnail: str
    viewCount: str


"""
    {
        "ID": 154726,
        "title": "브레인 데드부터 클락스 오리지널스까지, 이번 주 웍스아웃에서 만나볼 수 있는 팝업 3",
        "excerpt": "놓치면 무조건 후회할",
        "name": "worksout-brain-dead-timberland-clarks-originals",
        "publishedAt": "2023-10-16T08:00:00.000Z",
        "thumbnail": "content/uploads/posts/2023/10/13/main-112-aa55aa86-8556-4d3c-9dec-026a7fce60d5.jpg",
        "viewCount": "13799",
        "termRelationships.term_taxonomy_id": "445"
    },
"""

# @dataclasses.dataclass
# class Post:
#     ID: int
#     author: int
#     publishedAt: str
#     content: str
#     title: str
#     excerpt: str
#     status: str
#     preview: str
#     name: str
#     createUser: int
#     updateUser: int
#     type: str
#     thumbnail: str
#     bgImageForDesktop: str
#     bgImageForMobile: str
#     tags: List[str]
#     keywords: list
#     participantInfo: dict
#     viewCount: str
#     createdAt: str
#     updatedAt: str
#
#     cyclone_sliders: list = dataclasses.field(init=True, default=None)
#     basliders: List[object] = dataclasses.field(init=True, default=None)
#
#     def __repr__(self):
#         return f"Post(ID={self.ID}" \
#                f" author={self.author}" \
#                f" publishedAt={self.publishedAt}" \
#                f" content={self.content}" \
#                f" title={self.title}" \
#                f" exceprt={self.excerpt}" \
#                f" status={self.status}" \
#                f" name={self.name}" \
#                f" createdAt={self.createdAt}" \
#                f" updatedAt={self.updatedAt}" \
#                f" cyclone_sliders={self.cyclone_sliders}"
