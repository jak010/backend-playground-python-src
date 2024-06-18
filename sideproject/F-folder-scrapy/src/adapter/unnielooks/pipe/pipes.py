from src.adapter.abstract.abstract_pipe import AbstractScrapPipeLine


class UnnieLooksLinkScrapPipeLine(AbstractScrapPipeLine):
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


class UnnieLooksScrapPipeLine(AbstractScrapPipeLine):
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
