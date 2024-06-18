from src.app.remaker.command_query import RemakeCommand


class RemakeLoader:
    command = RemakeCommand()

    @classmethod
    def execute(cls, is_remake: bool, content: str, id: int):
        cls.command.update(is_remake=is_remake, content=content, id=id)
