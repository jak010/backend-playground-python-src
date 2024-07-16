from fastapi import FastAPI

from src.controller.endpoints import result_pattern_concept_router


class ResultPatternPocApplication:

    def __init__(self, title: str, description: str):
        self.app = FastAPI(
            title=title,
            description=description
        )

    def __call__(self, *args, **kwargs):
        self.app.include_router(result_pattern_concept_router)
        return self.app


application = ResultPatternPocApplication(
    title='FastAPI Result Pattern Proof of Concept',
    description="v0.1"
)
