from __future__ import annotations

import time
from typing import List, Optional, Dict, Tuple

from src.adapter import slack
from src.config.context import Transactional
from src.libs.resource.abstracts.abstract_usecase import (
    AbstractUsecase,
    AbstractUsecaseCRUDImplements,
    AbstrctUsecaseCrawlerImplements
)
from src.libs.resource.common.define import CONVERT
from src.libs.resource.common.universal_entity import UniversalEntity
from src.libs.resource.harpersbazaar.harpersbazaar_service import HarpersBazaarService
from src.libs.resource.post.post_entity import PostEntity
from src.libs.utils.content_creator import ContentCreator


class HarpersBazaarUsecase(
    AbstractUsecase,
    AbstractUsecaseCRUDImplements[UniversalEntity],
    AbstrctUsecaseCrawlerImplements
):

    def __init__(self):
        self.service = HarpersBazaarService()

    @Transactional()
    def get_content_list(
            self,
            page: int,
            item_per_page: int,
            sort_key: str,
            sort_type: str

    ) -> Optional[Tuple[List[UniversalEntity], int]]:
        return self.harpersbazaar_repository.find_by(
            page=page,
            item_per_page=item_per_page,
            sort_key=sort_key,
            sort_type=sort_type
        )

    @Transactional()
    def get_content(self, trace_id: str) -> Optional[UniversalEntity]:
        return self.harpersbazaar_repository.find_by_trace_id(
            trace_id=trace_id
        )

    @Transactional()
    def get_count(self) -> Optional[UniversalEntity]:
        return self.harpersbazaar_repository.get_count()

    @Transactional()
    def convert(self, trace_id: str) -> Dict[str, str]:
        harpersbazaar = self.harpersbazaar_repository.find_by_trace_id(trace_id=trace_id)
        if harpersbazaar is not None:
            post = self.post_repository.find_by_trace_id(trace_id=harpersbazaar.trace_id)
            if post is None:
                llm_content = ContentCreator().summary(harpersbazaar.content)

                self.post_repository.add(PostEntity.new(
                    trace_id=harpersbazaar.trace_id,
                    reference_link=harpersbazaar.reference_link,
                    thumbnail=harpersbazaar.thumbnail,
                    title=harpersbazaar.title,
                    content=llm_content,
                    keyword="harpersbazaar",
                    platform="harpersbazaar",
                    created_at=int(time.time())
                ))

                self.harpersbazaar_repository.update_on_convert(
                    trace_id=harpersbazaar.trace_id,
                    is_convert=CONVERT.ON
                )

                return {
                    "before_content": harpersbazaar.content,
                    "after_content": llm_content
                }

    @Transactional()
    def daily_collect(self):
        start_page = 1

        fetched_content_links = self.service.fetch_links(page=start_page)
        fetched_contents = [self.service.fetch_content(link) for link in fetched_content_links]
        fetched_contents_by_reference_ids = [int(fetched_content.reference_id) for fetched_content in fetched_contents]

        saved_contents = self.harpersbazaar_repository.find_by_refernece_ids(
            reference_ids=fetched_contents_by_reference_ids)
        saved_contents_by_reference_ids = [int(saved_content.reference_id) for saved_content in saved_contents]

        not_exist_contents_by_ids = self.service.not_exist_content_by_id(
            fetched_contents_reference_ids=fetched_contents_by_reference_ids,
            saved_contents_reference_ids=saved_contents_by_reference_ids
        )

        if len(not_exist_contents_by_ids) == 0:
            slack.send_to_slack(data=f"[INFO]HarpersBazaar Update Missing")
            return

        for not_exist_contents_by_id in not_exist_contents_by_ids:
            for fetched_content in fetched_contents:
                if int(not_exist_contents_by_id) == int(fetched_content.reference_id):
                    self.harpersbazaar_repository.add(universal_entity=UniversalEntity.new(
                        trace_id=fetched_content.trace_id,
                        reference_id=fetched_content.reference_id,
                        reference_date=self.service.to_datetime(fetched_content.reference_date).isoformat(),
                        reference_link=fetched_content.reference_link,
                        title=fetched_content.title,
                        content=fetched_content.content,
                        thumbnail=fetched_content.thumbnail
                    ))
        slack.send_to_slack(data=f"[INFO]HarpersBazaar Update after Count ...{len(not_exist_contents_by_ids)}")

    def all_collect(self):
        start_page = 1

        statistics = {"count": 0}
        while True:
            fetched_content_links = self.service.fetch_links(page=start_page)
            fetched_contents = [self.service.fetch_content(link) for link in fetched_content_links]

            with self.session.begin() as session:
                for fetched_content in fetched_contents:
                    reference_date_to_obj = self.service.to_datetime(reference_date=fetched_content.reference_date)

                    if self.service.is_stop_collect(reference_date=reference_date_to_obj):
                        slack.send_to_slack(data=f"[INFO]HarpersBazaar Collect ...{statistics['count']}")
                        return
                    else:
                        harpersbazaar = self.harpersbazaar_repository.find_by_refernece_id(
                            reference_id=int(fetched_content.reference_id))
                        if harpersbazaar is None:
                            self.harpersbazaar_repository.add(universal_entity=UniversalEntity.new(
                                trace_id=fetched_content.trace_id,
                                reference_id=fetched_content.reference_id,
                                reference_date=reference_date_to_obj.isoformat(),
                                reference_link=fetched_content.reference_link,
                                title=fetched_content.title,
                                content=fetched_content.content,
                                thumbnail=fetched_content.thumbnail
                            ))

                            statistics["count"] += 1

                session.commit()
            start_page += 1
