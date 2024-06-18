from dependency_injector.wiring import Provide

from src.app.otr.command_query import OTRCommand, OTRQuery
from src.app.otr.etl import OTRLoader, OTRTransform, OTRExtractor
from src.config.container import SlackContainer


class OTRRunner:
    notification = Provide[SlackContainer.notification]

    def __init__(self):
        self.extractor = OTRExtractor()
        self.loader = OTRLoader()

    def transport(self):
        urls = self.extractor.get_moive_pages(board_page=1)

        latest_saved_data = OTRQuery.get_latest()
        latest_fetch_data = []
        for url in urls:
            dto = OTRTransform(url).execute()
            if dto is not None:
                latest_fetch_data.append(dto)

        saved_datas = OTRLoader.fetch_data_for_storage(
            latest_saved_data=latest_saved_data,
            latest_fetch_data=latest_fetch_data
        )

        if saved_datas:
            try:
                for saved_data in saved_datas:
                    OTRCommand.save(saved_data)
                self.notification.send_message(data=f"[*]OTR COLLECT CATEGORY.. {len(saved_datas)}")
            except Exception as e:
                self.notification.send_message(data=f"[*]OTR COLLECT CAUTION.. {str(e.args[0])}")
