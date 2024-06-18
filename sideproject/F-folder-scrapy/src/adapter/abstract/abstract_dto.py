import abc
import uuid


class AbstractDto(metaclass=abc.ABCMeta):

    def __init__(self,
                 id: int = None,
                 trace_id: uuid.UUID = None,
                 reference_id: str | int = None,
                 reference_date: str = None,
                 title: str = None,
                 content: str = None,
                 reference_link: str = None,
                 thumbnail: str = None
                 ):
        self.id = self._hook_property(id)
        self.trace_id = trace_id if trace_id is not None else uuid.uuid4()
        self.reference_id = self._hook_property(reference_id)
        self.reference_date = self._hook_property(reference_date)
        self.reference_link = self._hook_property(reference_link)
        self.title = self._hook_property(title)
        self.content = self._hook_property(content)
        self.thumbnail = self._hook_property(thumbnail)

    def _hook_property(self, field):
        return field if field is not None else None

    def to_dict(self):
        return {
            "id": self.id,
            "trace_id": self.trace_id,
            "reference_id": self.reference_id,
            "reference_date": self.reference_date,
            "reference_link": self.reference_link,
            "title": self.title,
            "content": self.content,
            "thumbnail": self.thumbnail
        }

    def __repr__(self):
        return f"\n\n{self.__class__.__name__}(\n" \
               f"id={self.id},\n" \
               f"trace_id='{self.trace_id}',\n" \
               f"reference_id={self.reference_id},\n" \
               f"reference_date={self.reference_date},\n" \
               f"reference_link={self.reference_link}\n" \
               f"title={self.title},\n" \
               f"content={self.content},\n" \
               f"thumbnail={self.thumbnail})"
