import uuid
import datetime as dt
from typing import Type


class note ():
    __slots__ = ['_note']

    def __init__(self, **kwargs) -> None:
        '''
        Класс записи в блокноте.

        Аргументы конструктора:
            id: UUID            - идентификатор
            created: datetime   - дата создания записии
            modified: datetime  - дата изменения записи
            title: str          - заголовок записи
            text: str           - текст записи
        '''
        self._note = dict()
        self._note['id']: uuid.UUID = kwargs.get('id', uuid.uuid4())
        self._note['created']: dt.datetime = kwargs.get(
            'created', dt.datetime.now())
        self._note['modified']: dt.datetime = kwargs.get(
            'modified', self._note['created'])
        self._note['title']: str = kwargs.get('title', '')
        self._note['text']: str = kwargs.get('text', '')

    def __str__(self):
        result = ''
        for key, val in self._note.items():
            result += f'{key}: {val} \n'
        return result

    @property
    def note_id(self) -> uuid.UUID:
        '''
        Возвращает id записи
        '''
        return self._note['id']

    @property
    def note_created(self) -> dt.datetime:
        '''
        Возвращает дату создания записи
        '''
        return self._note['date_created']

    @property
    def note_modified(self) -> dt.datetime:
        '''
        Возвращает дату модификации записи
        '''
        return self._note['date_modified']

    @property
    def note_title(self) -> str:
        '''
        Возвращает заголовок записи
        '''
        return self._note['title']

    @note_title.setter
    def note_text(self, note_title: str) -> None:
        '''
        Меняет заголовок записи
        '''
        self._note['title'] = note_title
        self._note['date_modified'] = dt.datetime.now()

    @property
    def note_text(self) -> str:
        '''
        Возвращает текст записи
        '''
        return self._note['text']

    @note_text.setter
    def note_text(self, note_text: str) -> None:
        '''
        Меняет текст записи
        '''
        self._note['text'] = note_text
        self._note['date_modified'] = dt.datetime.now()

    def to_list(self) -> list:
        '''
        Возвращает запись в виде списка
        '''
        return self._note.values()

    def to_dict(self) -> dict:
        '''
        Возвращает запись в виде словаря
        '''
        return self._note
