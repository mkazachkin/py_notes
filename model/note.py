import uuid
import datetime as dt
import pandas as pd


class note ():
    __slots__ = ['_note_series']

    def __init__(self, **kwargs) -> None:
        '''
        Класс записи в блокноте.

        Аргументы конструктора:
            note_id: UUID                   - идентификатор записи
            note_date_creation: datetime    - дата и время создания записи
            note_date_change: datetime      - дата и время модификации записи
            note_title: str                 - заголовок записи
            note_text: str                  - текст записи
        '''
        _note_id: uuid.UUID = kwargs.get('note_id', uuid.uuid4())
        _note_date_creation: dt.datetime = kwargs.get(
            'note_date_creation', dt.datetime.now())
        _note_date_change: dt.datetime = kwargs.get(
            'note_date_change', dt.datetime.now())
        _note_title: str = kwargs.get('note_title', '')
        _note_text: str = kwargs.get('note_text', '')
        self._note_series: pd.Series = pd.Series([_note_id, _note_date_creation, _note_date_change, _note_title, _note_text],
                                                 index=['id', 'date_creation', 'date_change', 'title', 'text'])

    def __str__(self):
        result = ''
        for idx, val in self._note_series.items():
            result += f'{idx}:\t{val} \n'
        return result

    note_series = property()

    @note_series.getter
    def get_note_series(self) -> pd.Series:
        '''
        Возвращает запись
        '''
        return self._note_series

    @note_series.setter
    def set_note_series(self, _note_series: pd.Series) -> None:
        '''
        Меняет запись
        '''
        self._note_series = _note_series
