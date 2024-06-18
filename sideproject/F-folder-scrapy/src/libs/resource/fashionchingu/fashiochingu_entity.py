import copyimport dataclassesimport jsonfrom src.adapter.fashionchingu.api.libs.dto import FashionChinguDtofrom src.libs.resource.common.define import CONVERTfrom src.libs.resource.common.universal_entity import UniversalEntityfrom src.libs.resource.fashionchingu.fashionchingu_service import FashionChinguService@dataclasses.dataclassclass FashionChinguEntity(UniversalEntity):    def __repr__(self):        _content = copy.deepcopy(self.content)        _repr = self.__class__.__name__ + "("        _repr += json.dumps({            "id": self.id,            "trace_id": self.trace_id,            "is_convert": self.is_convert,            "reference_id": self.reference_id,            "reference_date": self.reference_date.isoformat(),            "reference_link": self.reference_link,            "title": self.title,            "content": _content[0:7] + f"...({len(_content)}size)",            "thumbnail": self.thumbnail        }, ensure_ascii=False, indent=4)        _repr += ")"        return _repr    @classmethod    def from_dto(cls, fashionchingu_dto: FashionChinguDto):        return cls(            id=None,            trace_id=fashionchingu_dto.trace_id,            reference_id=fashionchingu_dto.reference_id,            reference_date=FashionChinguService.to_datetime(reference_date=fashionchingu_dto.reference_date),            reference_link=fashionchingu_dto.reference_link,            thumbnail=fashionchingu_dto.thumbnail,            is_convert=CONVERT.OFF.value,            title=fashionchingu_dto.title,            content=fashionchingu_dto.content        )