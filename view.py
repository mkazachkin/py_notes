from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll, ListView, ListItem
from textual.widgets import Header, Static
from controller import sheets


class py_notes():
    __slots__ = ['_nb']

    def __init__(self):
        self._nb = sheets()

    def get_status(self) -> None:
        print(f'Текущее количество записей: {self._nb.records_num}')

    def show_menu():
        print('''
        1. Добавить запись
        2. Просмотреть все записи
        3. Просмотреть записи за конкретные даты
        4. Загрузить данные из csv-файла
        5. Загрузить данные из json-файла
        6. Сохранить данные в csv-файл
        7. Сохранить данные в json-файл
        X. Выйти из программы

        ''')

        None
