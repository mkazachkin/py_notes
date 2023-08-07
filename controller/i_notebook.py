from uuid import uuid4
from abc import ABCMeta, abstractmethod
import model.note as note


class i_notebook():
    __metaclass_ = ABCMeta

    @abstractmethod
    def get_notes(note_id_list: list = [], **kwargs) -> set:
        '''
        Возвращает сет записей, выбранных из блокнота в зависимости от заданных параметров.
        Метод, выполненный с пустыми аргументами, вернет все записи в блокноте.

        Аргументы:
            note_id_list: list: uuid4       - список id записей. Может быть пустым.
            note_date_start: datetime       - начальная дата записей.
            note_date_end: datetime         - конечная дата записей.
            note_date_set: set: datetime    - сет дат записей.
            search_title_string: str        - поисковая строка в заголовке записи.
            search_text_string: str         - поисковая строка в тексте записи.
        '''

    @abstractmethod
    def del_notes(note_id_list: list = [], **kwargs) -> None:
        '''
        Удаляет записи в блокноте в зависимости от заданных параметров.
        Метод, выполненный с пустыми аргументами, удалит все записи в блокноте.

        Аргументы:
            note_id_list: list: uuid4       - список id записей. Может быть пустым.
            note_date_start: datetime       - начальная дата записей.
            note_date_end: datetime         - конечная дата записей.
            note_date_set: set: datetime    - сет дат записей.
            search_title_string: str        - поисковая строка в заголовке записи.
            search_text_string: str         - поисковая строка в тексте записи.
        '''

    @abstractmethod
    def add_note(new_note: note) -> uuid4:
        '''
        Добавляет запись в блокнот.
        Возвращает id запииси в блокноте
        '''
