from __future__ import annotations

from src.adapter.abstract.abstract_pipe import AbstractScrapPipeLine


class KrazeMediaScrapPipeLine(AbstractScrapPipeLine):

    def start(self):

        self._data = None
        for f in self.filters:
            if self._data is None:
                self._data = f.execute()
            else:
                self._data = f.execute(self._data)
        return self._data

    def get_result(self):
        return self._data
