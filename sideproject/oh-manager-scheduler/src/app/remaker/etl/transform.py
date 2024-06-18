from src.app.remaker.prompts import ContentsCreateLLM


class RemakerTransform:

    def __init__(self):
        self.llm = ContentsCreateLLM()

    def execute(self, content):
        return self.llm.factory(content=content)
