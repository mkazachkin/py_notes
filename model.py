import uuid
import datetime


class sheets ():
    __slots__ = ['_header', '_sheets']

    def __init__(self, **kwargs) -> None:
        '''
        Класс страниц блокнота.

        Аргументы конструктора:
            sheets: list    - список записей вместе с id
        '''
        self._header = {'created': 0, 'modified': 1, 'title': 2, 'text': 3}
        self._sheets = dict()
        if 'sheets' in kwargs:
            for sheet in kwargs.get('sheets'):
                self._note[sheet[0]: sheet[1:]]
        self._sort_sheets()

    def add(self, title: str, text: str) -> None:
        _time = datetime.datetime.now().timestamp()
        self._sheets[uuid.uuid4().int] = [_time, _time, title, text]

    def mod(self, id: int, title: str, text: str) -> None:
        _time = datetime.datetime.now().timestamp()
        self._sheets[id] = [self._sheets[id][0], _time, title, text]
        self._sort_sheets()

    def rem(self, id: int) -> None:
        del self._sheets[id]
        self._sort_sheets()

    def get(self) -> dict:
        return self._sheets

    def head(self) -> list:
        return self._header.keys()

    def _sort_sheets(self, column: str = 'created') -> None:
        col: int = 0
        if column in self._header.keys():
            col = self._header[column]
        self._sheets = {key: val for key, val in
                        sorted(self._sheets.items(),
                               key=lambda rec: rec[1][col])}
