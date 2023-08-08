import os
from controller import sheets
from model import note
from colorama import init, Fore, Back, Style


class py_notes():
    # __slots__ = ['_nb', '_width']

    def __init__(self):
        init()
        os.get_terminal_size()
        self._nb = sheets()
        self._width = os.get_terminal_size().columns

    def get_status(self) -> None:
        output_str: str = Fore.YELLOW + Back.LIGHTBLACK_EX + \
            f' Текущее количество записей: {self._nb.records_num()}'

        print(output_str.ljust(self._width) + Style.RESET_ALL)

    def choose_menu(self) -> int:
        menu_items = {
            '1': 'Добавить запись',
            '2': 'Просмотреть все записи',
            '3': 'Просмотреть записи за конкретные даты',
            '4': 'Загрузить данные из csv-файла',
            '5': 'Загрузить данные из json-файла',
            '6': 'Сохранить данные в csv-файл',
            '7': 'Сохранить данные в json-файл',
            '8': 'Выйти из программы'
        }
        flag: bool = False
        while not flag:
            self.cls()
            self.get_status()
            for num, name in menu_items.items():
                print(f' {num}. {name}')
            choose: str = input('Введите пункт меню: ')
            if choose in menu_items.keys():
                flag = True
        return int(choose)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_note(self) -> note:


a = py_notes()
a.choose_menu()
print()
