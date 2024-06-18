import time

from src.app.abstarct import AbstractCommandQuery


class RemakeCommand(AbstractCommandQuery):
    update_sql = """
        UPDATE `auditions` SET is_remake = :is_remake, content=:content, modified_at=:modified_at WHERE id = :id;     
    """

    @classmethod
    def update(cls, is_remake: bool, content: str, id: int):
        cls.session.execute(cls.update_sql, {
            "is_remake": is_remake,
            "content": content,
            "id": id,
            "modified_at": int(time.time())
        })
        cls.session.commit()
