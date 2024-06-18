import os
from abc import ABCMeta, abstractmethod
from typing import List

from dotenv import load_dotenv
from langchain.chains import LLMChain
# from langchain.cache import InMemoryCache
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
# from langchain.globals import set_llm_cache
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# set_llm_cache(InMemoryCache())


load_dotenv()

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']


def get_docs(text: str):
    docs = []
    for text in text.splitlines():
        docs.append(Document(page_content=text))
    return docs


class AbstractCreator(metaclass=ABCMeta):

    def __init__(self):
        self._model = 'gpt-3.5-turbo-16k-0613'
        # self._model = 'text-davinci-003'
        self._temperature = 0

        self.llm = ChatOpenAI(
            temperature=self._temperature,
            model_name=self._model,
            openai_api_key=OPENAI_API_KEY
        )

    @abstractmethod
    def prompt(self, *args, **kwargs): ...


class HTMLCreator(AbstractCreator):

    def prompt(self):
        template = """아래 내용을 요약해줘
        {text}
        """
        return PromptTemplate(template=template, input_variable=['text'])

    def text_splitter(self):
        return CharacterTextSplitter(
            separator="\n\n",
            chunk_size=3000,  # 쪼개는 글자수
            chunk_overlap=300,  # 오버랩 글자수
            length_function=len,
            is_separator_regex=False,
        )


class ContentCreator(AbstractCreator):

    def prompt(self):
        template01 = """아래 내용을 "서론","본론","결론"에 따라 요약하고 url이나 link는 각 요약에 삽입해줘\n
        {text} 
        """
        return PromptTemplate(template=template01, input_variables=['text'])

    def chain(self):
        return load_summarize_chain(
            self.llm,
            prompt=self.prompt(),
            verbose=True
        )

    def summary(self, text):
        return self.chain().run(get_docs(text))


class AutoGenerateContent(AbstractCreator):
    CHUNK_SIZE = 2000

    @property
    def text_spliiter(self):
        return RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE,
            chunk_overlap=0,
        )

    def to_docs(self, text) -> List[Document]:
        docs = []
        for text in self.text_spliiter.split_text(text):
            docs.append(Document(page_content=text))
        return docs

    def prompt(self, prompt_text):
        return PromptTemplate(template=prompt_text, input_variables=['text'])

    def make_content(self, text):
        chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt(prompt_text=""""아래 내용을 3000자 이상으로 '서론','결론','본론'으로 요약해줘\n {text}"""),
            verbose=True
        )
        return chain.run(text=text)


class KeywordCreator(AbstractCreator):

    def prompt(self):
        template01 = """아래 내용에 대해 ','를 구분자로 키워드를 나열해줘 \n
        {text} 
        """
        return PromptTemplate(template=template01, input_variables=['text'])

    def chain(self):
        return load_summarize_chain(
            self.llm,
            prompt=self.prompt(),
            verbose=True
        )

    def summary(self, text):
        return self.chain().run(get_docs(text))
