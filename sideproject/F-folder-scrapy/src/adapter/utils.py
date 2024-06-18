from abc import ABCMeta, abstractmethod

from typing import List

import requests
from fake_useragent import UserAgent

import cloudscraper


class ByPassRequestMixin:
    request = cloudscraper.create_scraper()


class RequestMixin:

    def get(self, url, params=None):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response

    def post(self, url, data):
        response = requests.post(
            url=url,
            headers={"User-Agent": UserAgent().random},
            data=data
        )
        if response.status_code == 200:
            return response
