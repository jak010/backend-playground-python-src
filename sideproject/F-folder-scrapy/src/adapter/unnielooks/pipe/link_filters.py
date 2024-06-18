from bs4 import BeautifulSoup, element
from src.adapter.abstract.abstract_pipe import AbstractScrapFilter


class InitContentTagFilter(AbstractScrapFilter):

    def __init__(self, html_source: str):
        self.html_source = html_source

    def execute(self):
        soup = BeautifulSoup(self.html_source, "html.parser") \
            .find("div", {"class": "blog-articles"})
        return soup


class ExtractContentTagFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        data = []

        element_tag = html_element.findAll('div')

        for elem in element_tag:
            if elem := elem.find('a'):
                data.append(elem['href'])

        return data


class ExtractContentLinkFilter(AbstractScrapFilter):

    def execute(self, html_element: element.Tag):
        links = []

        element_tag = html_element.findAll("a", {"class": "full-unstyled-link"})
        for elem in element_tag:
            links.append("https://unnielooks.com/en-kr/blogs/news/" + elem['href'].split('/')[-1])

        links = list(set(links))
        return links
