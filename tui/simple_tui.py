import os
import re
from colorama import init, Fore, Back, Style
from typing import TypeVar

key_type = TypeVar('key_type')


class simple_tui():

    __slots__ = ['width']

    def __init__(self) -> None:
        init()
        self.width = os.get_terminal_size().columns

    def get_menu_choise(self, menu_items: dict[key_type, any], info_str: str = '', do_cls: bool = True, vertical: bool = True) -> key_type:
        '''
            Отображает пункты меню из словаря и возвращает идентификатор выбранного пункта меню

            Аргументы:
                menu_items: dict[key_type, any]    - словарь пунктов меню, где ключами являются id пунктов
                info_str: str               - строка информационная
                do_cls: bool                - выполнять очистку экрана (да, по-умолчанию)
                vertical: bool              - вертикальное меню или горизоонтальное (вертикальное, по-умолчанию)
            '''
        menu_keys = dict[key_type, any]()
        flag: bool = False
        while not flag:
            _i: int = 1
            menu: str = ''
            if do_cls:
                self.cls()
            if info_str != '':
                self.print_info(info_str, 'center')
            for key in menu_items.keys():
                menu_keys[str(_i)] = key
                menu += f' {_i}. {menu_items[key]}'
                if vertical:
                    menu += '\n'
                else:
                    menu += ' | '
                _i += 1
            menu += f' 0. Выход'
            print(menu)
            choise: str = input('Введите пункт меню: ')
            if choise in menu_keys.keys():
                flag = True
            elif choise == '0':
                return None
        return menu_keys[choise]

    def get_yes_no_menu(self, ask_str: str = '') -> bool:
        '''
        Запрашивает пользователя на совершение действия и возвращает ответ

        Аргументы:
            ask_str: str    - вопрос пользователю
        '''
        self.cls()
        if ask_str == '':
            ask_str = 'Вы уверены?'
        ask_str = ask_str.rjust(
            (self.width-len(ask_str))//2 + len(ask_str)).ljust(self.width)
        yn_str = '(y/N)'
        yn_str = yn_str.rjust(
            (self.width-len(yn_str))//2 + len(yn_str)).ljust(self.width)
        print((Fore.BLACK + Back.LIGHTRED_EX + ask_str + Style.RESET_ALL))
        print((Fore.BLACK + Back.LIGHTRED_EX + yn_str + Style.RESET_ALL))
        return input().lower() == 'y'

    def print_info(self, info_str: str, align: str = 'left', width: int = 0) -> None:
        '''
        Выводит информационную строку.

        Аргументы:
            info-str: str   - содержимое информационной строки
            align: str      - выравнивание строки: left, center, right
            width: int      - ширина информационной строки. Не должна быть больше ширины терминала или меньше 12 символов.
                            В противном случае и выводится на всю ширину терминала
        '''
        if width < 12 or width > self.width:
            width = self.width
        lines = info_str.split('\n')
        for i in range(len(lines)):
            lines[i] = re.sub(' +', ' ', lines[i]).strip()

        i = 0
        flag = False
        while not flag:
            if len(lines[i]) > width - 2:
                words = lines[i][:width - 2].split()
                if len(words) > 1:
                    words.pop()
                    newline = ' '.join(words)
                else:
                    newline = words[0]
                lines.insert(i + 1, lines[i][len(newline) + 1:])
                lines[i] = newline
            i += 1
            if i == len(lines):
                flag = True

        for line in lines:
            if align == 'right':
                line = (line + ' ').rjust(width)
            elif align == 'center':
                line = line.rjust((width-len(line))//2 +
                                  len(line)).ljust(width)
            else:
                line = (' ' + line).ljust(width)
            print((Fore.YELLOW + Back.LIGHTBLACK_EX + line + Style.RESET_ALL))

    def cls(self):
        '''
        Очищает консоль как в Windows, так и в *nix
        '''
        os.system('cls' if os.name == 'nt' else 'clear')
