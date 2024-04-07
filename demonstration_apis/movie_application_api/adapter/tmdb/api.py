from typing import List

import requests

from adapter.tmdb.dto.movie_list_dto import MoiveDto


class TmdbAPI:

    def __init__(self, api_read_key: str):
        self.api_read_key = api_read_key
        self.base_headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_read_key}"
        }

        self._base_url = "https://api.themoviedb.org"

    def get_movie_list(self) -> List[MoiveDto]:
        """ https://developer.themoviedb.org/reference/changes-movie-list """
        _endpoint = "/3/movie/changes?page=1"

        resp = requests.get(self._base_url + _endpoint, headers=self.base_headers)
        if resp.status_code == 200:
            data = resp.json()
            return [MoiveDto(**item) for item in data['results']]
