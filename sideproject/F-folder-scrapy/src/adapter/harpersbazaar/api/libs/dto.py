import dataclasses

from src.adapter.abstract.abstract_dto import AbstractDto


class HarpersBazaarDto(AbstractDto):

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

    def __repr__(self):
        return f"\n\n{self.__class__.__name__}(\n" \
               f"id={self.id},\n" \
               f"trace_id='{self.trace_id}',\n" \
               f"reference_id={self.reference_id},\n" \
               f"reference_date={self.reference_date},\n" \
               f"reference_link={self.reference_link}\n" \
               f"title={self.title},\n" \
               f"content={self.content[0:5]}... ({len(self.content)}..sizes),\n" \
               f"thumbnail={self.thumbnail})"
