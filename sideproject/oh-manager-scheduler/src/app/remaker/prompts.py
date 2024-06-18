from langchain.schema import SystemMessage, HumanMessage

from langchain_community.chat_models import ChatOpenAI

from src.config.base import OPEN_AI_APIKEY

TEMPERAUTE = 0
MAX_TOKEN_VALUE = 4096
GPT_35_TURBO = 'gpt-3.5-turbo-16k'


class ContentsCreateLLM:
    llm_model = ChatOpenAI(
        temperature=TEMPERAUTE,
        model_name=GPT_35_TURBO,
        max_tokens=MAX_TOKEN_VALUE,
        openai_api_key=OPEN_AI_APIKEY
    )

    @classmethod
    def factory(cls, content):
        messages = [
            SystemMessage(content="당신은 오디션 지원자에게 오디셤 모집 내용을 효과적으로 전달할 수 있도록 글쓰는 작업을 돕는 것입니다."),
            SystemMessage(content="결과는 한국어로 번역해주세요"),
            HumanMessage(content=f"본문 : ```{content}```"),
            HumanMessage(content="""
                본문의 내용을 오디션 지원자에게 효과적으로 전달할 수 있도록 "제목", "내용","모집배역" 순으로 요약해주고 제목은 내용을 기반으로 작성해주세요.
                본문의 내용에 URL만 존재한다면 해당 작업은 진행하지 마세요.
                """)
        ]

        return cls.llm_model(messages).content
