import dataclasses
import time


@dataclasses.dataclass
class OTRAuditionDto:
    vid: str
    title: str
    content: str
    category: str
    reward: str
    link: str
    end_date: str
    author: str
    created_at: int
    modified_at: int

    @classmethod
    def new(
            cls,
            vid=None,
            title=None,
            content=None,
            category=None,
            reward=None,
            link=None,
            end_date=None,
            author=None,
    ):
        return cls(
            vid=vid,
            title=title,
            content=content,
            category=category,
            reward=reward,
            link=link,
            end_date=end_date,
            author=author,
            created_at=int(time.time()),
            modified_at=int(time.time())
        )

    def to_dict(self):
        return dataclasses.asdict(self)

    def __repr__(self):
        return f"OTRAuditionDto(vid={self.vid}, title={self.title}, end_date={self.end_date})\n"
