from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import List

from src.adapter.abstract.abstract_dto import AbstractDto


class VogueKoreaDto(AbstractDto):
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
            thumbnail=None,
    ):
        return cls(
            id=id,
            trace_id=trace_id,
            reference_id=reference_id,
            reference_date=reference_date,
            reference_link=reference_link,
            title=title,
            content=content,
            thumbnail=thumbnail,
        )

    def __lt__(self, other):
        return int(self.reference_id) < int(other.reference_id)


@dataclass
class CfPostCredit:
    desc: str
    title: str

    @staticmethod
    def from_dict(obj: Any) -> "CfPostCredit":
        _desc = str(obj.get("desc"))
        _title = str(obj.get("title"))
        return CfPostCredit(_desc, _title)


@dataclass
class CfPostEditor:
    ID: int
    display_name: str
    nickname: str
    user_avatar: str
    user_description: str
    user_email: str
    user_firstname: str
    user_lastname: str
    user_nicename: str
    user_registered: str
    user_url: str

    @staticmethod
    def from_dict(obj: Any) -> "CfPostEditor":
        _ID = int(obj.get("ID"))
        _display_name = str(obj.get("display_name"))
        _nickname = str(obj.get("nickname"))
        _user_avatar = str(obj.get("user_avatar"))
        _user_description = str(obj.get("user_description"))
        _user_email = str(obj.get("user_email"))
        _user_firstname = str(obj.get("user_firstname"))
        _user_lastname = str(obj.get("user_lastname"))
        _user_nicename = str(obj.get("user_nicename"))
        _user_registered = str(obj.get("user_registered"))
        _user_url = str(obj.get("user_url"))
        return CfPostEditor(
            _ID,
            _display_name,
            _nickname,
            _user_avatar,
            _user_description,
            _user_email,
            _user_firstname,
            _user_lastname,
            _user_nicename,
            _user_registered,
            _user_url,
        )


@dataclass
class CurrentPost:
    cf_content_source: str
    cf_post_credits: List[CfPostCredit]
    cf_post_editor: List[CfPostEditor]
    cf_post_editor_etc: str
    cf_post_main_flag: bool
    cf_post_type: str
    permalink: str
    post_date: str
    post_editors: str
    post_id: str
    post_no: str
    post_terms: str
    post_thumbnail_url: str
    post_title: str
    seo_setting: SeoSetting
    cf_content_source_url: str

    @staticmethod
    def from_dict(obj: Any) -> "CurrentPost":
        _cf_content_source = str(obj.get("cf_content_source"))
        _cf_post_credits = ""
        _cf_post_editor = ""
        _cf_post_editor_etc = str(obj.get("cf_post_editor_etc"))
        _cf_post_main_flag = bool(obj.get("cf_post_type"))
        _cf_post_type = str(obj.get("cf_post_type"))
        _permalink = str(obj.get("permalink"))
        _post_date = str(obj.get("post_date"))
        _post_editors = str(obj.get("post_editors"))
        _post_id = str(obj.get("post_id"))
        _post_no = str(obj.get("post_no"))
        _post_terms = str(obj.get("post_terms"))
        _post_thumbnail_url = str(obj.get("post_thumbnail_url"))
        _post_title = str(obj.get("post_title"))
        _seo_setting = SeoSetting.from_dict(obj.get("seo_setting"))
        _cf_content_source_url = str(obj.get("cf_content_source_url"))
        return CurrentPost(
            _cf_content_source,
            _cf_post_credits,
            _cf_post_editor,
            _cf_post_editor_etc,
            _cf_post_main_flag,
            _cf_post_type,
            _permalink,
            _post_date,
            _post_editors,
            _post_id,
            _post_no,
            _post_terms,
            _post_thumbnail_url,
            _post_title,
            _seo_setting,
            _cf_content_source_url,
        )


@dataclass
class CurrentTerm:
    tax1_term: Tax1Term
    tax2_term: Tax2Term
    terms_depth2: List[TermsDepth2]

    @staticmethod
    def from_dict(obj: Any) -> "CurrentTerm":
        _tax1_term = Tax1Term.from_dict(obj.get("tax1_term"))
        _tax2_term = Tax2Term.from_dict(obj.get("tax2_term"))
        _terms_depth2 = [TermsDepth2.from_dict(y) for y in obj.get("terms_depth2")]
        return CurrentTerm(_tax1_term, _tax2_term, _terms_depth2)


@dataclass
class FashionTrends:
    count_posts: str
    current_posts: List[CurrentPost]
    current_term: CurrentTerm

    @staticmethod
    def from_dict(obj: Any) -> "FashionTrends":
        _count_posts = str(obj.get("count_posts"))
        _current_posts = [
            CurrentPost.from_dict(y) for y in obj.get("current_posts", {})
        ]
        _current_term = CurrentTerm.from_dict(obj.get("current_term"))
        return FashionTrends(_count_posts, _current_posts, _current_term)


@dataclass
class SeoSetting:
    seo_desc: str
    seo_title: str
    sns_desc: str
    sns_image: bool
    sns_title: str

    @staticmethod
    def from_dict(obj: Any) -> "SeoSetting":
        _seo_desc = ""
        _seo_title = ""
        _sns_desc = ""
        _sns_image = ""
        _sns_title = ""
        return SeoSetting(_seo_desc, _seo_title, _sns_desc, _sns_image, _sns_title)


@dataclass
class Tax1Term:
    count: int
    description: str
    filter: str
    name: str
    parent: int
    slug: str
    taxonomy: str
    term_group: int
    term_id: int
    term_taxonomy_id: int

    @staticmethod
    def from_dict(obj: Any) -> "Tax1Term":
        _count = int(obj.get("count"))
        _description = str(obj.get("description"))
        _filter = str(obj.get("filter"))
        _name = str(obj.get("name"))
        _parent = int(obj.get("parent"))
        _slug = str(obj.get("slug"))
        _taxonomy = str(obj.get("taxonomy"))
        _term_group = int(obj.get("term_group"))
        _term_id = int(obj.get("term_id"))
        _term_taxonomy_id = int(obj.get("term_taxonomy_id"))
        return Tax1Term(
            _count,
            _description,
            _filter,
            _name,
            _parent,
            _slug,
            _taxonomy,
            _term_group,
            _term_id,
            _term_taxonomy_id,
        )


@dataclass
class Tax2Term:
    count: int
    description: str
    filter: str
    name: str
    parent: int
    slug: str
    taxonomy: str
    term_group: int
    term_id: int
    term_taxonomy_id: int

    @staticmethod
    def from_dict(obj: Any) -> "Tax2Term":
        _count = int(obj.get("count"))
        _description = str(obj.get("description"))
        _filter = str(obj.get("filter"))
        _name = str(obj.get("name"))
        _parent = int(obj.get("parent"))
        _slug = str(obj.get("slug"))
        _taxonomy = str(obj.get("taxonomy"))
        _term_group = int(obj.get("term_group"))
        _term_id = int(obj.get("term_id"))
        _term_taxonomy_id = int(obj.get("term_taxonomy_id"))
        return Tax2Term(
            _count,
            _description,
            _filter,
            _name,
            _parent,
            _slug,
            _taxonomy,
            _term_group,
            _term_id,
            _term_taxonomy_id,
        )


@dataclass
class TermsDepth2:
    count: int
    description: str
    filter: str
    name: str
    parent: int
    slug: str
    taxonomy: str
    term_group: int
    term_id: int
    term_taxonomy_id: int

    @staticmethod
    def from_dict(obj: Any) -> "TermsDepth2":
        _count = int(obj.get("count"))
        _description = str(obj.get("description"))
        _filter = str(obj.get("filter"))
        _name = str(obj.get("name"))
        _parent = int(obj.get("parent"))
        _slug = str(obj.get("slug"))
        _taxonomy = str(obj.get("taxonomy"))
        _term_group = int(obj.get("term_group"))
        _term_id = int(obj.get("term_id"))
        _term_taxonomy_id = int(obj.get("term_taxonomy_id"))
        return TermsDepth2(
            _count,
            _description,
            _filter,
            _name,
            _parent,
            _slug,
            _taxonomy,
            _term_group,
            _term_id,
            _term_taxonomy_id,
        )

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
