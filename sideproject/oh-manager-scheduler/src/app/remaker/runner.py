from src.app.remaker.etl import RemakerExtractor, RemakerTransform, RemakeLoader

from dependency_injector.wiring import Provide

from src.config.container import SlackContainer


class RemakeRunner:
    notification = Provide[SlackContainer.notification]

    extractor = RemakerExtractor()
    transform = RemakerTransform()
    loader = RemakeLoader()

    @classmethod
    def execute(cls):
        updates = []

        datas = cls.extractor.get_before_remake()

        if datas:
            for data in datas:
                after_content = cls.transform.execute(content=data['content'])
                updates.append({'id': data['id'], 'content': after_content})

            for update in updates:
                cls.notification.send_message(data=f"[*]PROMPTRED AUDTION_ID.. {update['id']}")
                cls.loader.execute(
                    is_remake=True,
                    id=update['id'],
                    content=update['content'],
                )
