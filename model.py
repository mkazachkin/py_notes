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
        self._header = {'id': -1, 'created': 0,
                        'modified': 1, 'title': 2, 'text': 3}
        self._sheets = kwargs.get('sheets', dict())
        self._sort_sheets()

    def add(self, title: str, text: str) -> None:
        '''
        Добавляет новую запись в блокнот.

        Аргументы:
            title: str  - заголовок записи
            text: str   - текст записи
        '''
        _time = datetime.datetime.now().timestamp()
        self._sheets[uuid.uuid4().int] = [_time, _time, title, text]

    def mod(self, id: int, title: str, text: str) -> None:
        '''
        Изменяет запись в блокноте.

        Аргументы:
            id: int     - идентификатор записи
            title: str  - заголовок записи
            text: str   - текст записи
        '''
        _time = datetime.datetime.now().timestamp()
        self._sheets[id] = [self._sheets[id][0], _time, title, text]
        self._sort_sheets()

    def rem(self, id: int) -> None:
        '''
        Удаляет запись в блокноте.

        Аргументы:
            title: str  - заголовок записи
            text: str   - текст записи
        '''
        del self._sheets[id]

    @property
    def sheets(self) -> dict:
        '''
        Возвращает блокнот в виде словаря
        '''
        return self._sheets

    @property
    def head(self) -> list:
        '''
        Возвращает заголовки полей блокнота
        '''
        return list(self._header.keys())

    def _sort_sheets(self, column: str = 'created') -> None:
        '''
        Выполняет пересборку словаря по одному из критериев

        Аргументы:
            column: str - название поля словаря, по которому производится сортировка
        '''
        col: int = 0
        if column in self._header.keys():
            col = self._header[column]
        self._sheets = {key: val for key, val in
                        sorted(self._sheets.items(),
                               key=lambda rec: rec[1][col])}
