import os
import datetime
from controller import notebook
from colorama import init, Fore, Back, Style


class py_notes():
    __slots__ = ['_nb', '_width', '_cfg', '_notebook_path']

    def __init__(self):
        init()
        self._nb = notebook()
        self._width = os.get_terminal_size().columns
        self._cfg = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'main.cfg')
        self._notebook_path = ''
        try:
            with open(self._cfg, 'r') as cfg_file:
                self._notebook_path = cfg_file.read()
        except EnvironmentError:
            self.save_cfg(self)
        if self._notebook_path != '':
            self.load_from_csv(self._notebook_path)

    def get_menu_choise(self, menu_items: dict, do_smth=lambda *args: None, vertical: bool = True, *args, **kwargs):
        '''
        Отображает пункты меню из словаря и возвращает идентификатор выбранного пункта меню

        Аргументы:
            menu_items: dict    - словарь пунктов меню, где ключами являются id пунктов
            do_smth:            - функция, которая что-то делает после очистки экрана, но до отображения меню
        '''
        menu_keys = dict()
        flag: bool = False
        while not flag:
            counter: int = 1
            menu: str = ''
            if not kwargs.get('donot_cls'):
                self.cls()
            if args:
                do_smth(args)
            else:
                do_smth()
            for key in menu_items.keys():
                menu_keys[str(counter)] = key
                menu += f' {counter}. {menu_items[key]}'
                if vertical:
                    menu += '\n'
                else:
                    menu += ' | '
                counter += 1
            menu += f' 0. Выход'
            print(menu)
            choise: str = input('Введите пункт меню: ')
            if choise in menu_keys.keys():
                flag = True
            elif choise == '0':
                return None
        return menu_keys[choise]

    def cls(self):
        '''
        Очищает консоль как в Windows, так и в *nix
        '''
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_menu(self) -> int:
        menu_items = {
            1: 'Добавить запись',
            2: 'Просмотреть все записи',
            3: 'Просмотреть записи за конкретные даты',
            4: 'Указать путь к csv-файлу и загрузить данные',
            5: 'Указать путь к csv-файлу и сохранить данные',
            6: 'Сохранить',
        }
        # В моей Alt Linux установлен "древний" Python 3.9, поэтому без match-case
        menu_choise = 0
        while menu_choise != None:
            if menu_choise == 1:
                self.add_record()
            if menu_choise == 2:
                self.records_menu()
            if menu_choise == 3:
                self.records_menu(ask_first_date=True, ask_last_date=True)
            if menu_choise == 4:
                self.load_from_csv()
            if menu_choise == 5:
                self.save_to_csv()
            if menu_choise == 6:
                self.save_to_csv(self._notebook_path)
            info_str: str = ''
            if self._notebook_path != '':
                info_str += f'Файл БД: {self._notebook_path[12 - self._width//2:]} '.rjust(
                    self._width)
            info_str += (f'Текущее количество записей: {self._nb.pages} ').rjust(
                self._width)
            menu_choise = self.get_menu_choise(
                menu_items, lambda *args: print(Fore.YELLOW + Back.LIGHTBLACK_EX + args[0][0] + Style.RESET_ALL), True, info_str)

    def add_record(self, rec_id: int = -1) -> None:
        '''
        Выводит форму ввода записи и записывает ее в блокнот

        Аргументы:
            rec_id: int     - идентификатор записи, которую нужно заменить
        '''
        self.cls()
        title: str = input('Введите заголовок записи: ')
        print('Введите текст записи. Пустая строка означает окончание записи.')
        text: str = ''
        flag: bool = False
        while not flag:
            line = input()
            if line:
                text += line + '\n'
            else:
                flag = True
        if rec_id < 0:
            self._nb.add_sheet(title, text[:-1])
        else:
            self._nb.update_sheet(rec_id, title, text)

    def records_menu(self, **kwargs) -> None:
        '''
        Выводит список записей.

        Аргументы:
            ask_first_date: bool    - запрос начальной даты
            ask_last_date: bool     - запрос конечной даты
        '''
        menu_choise = 0
        flag = False
        start_date = '1970-01-01'
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        if kwargs.get('ask_first_date') or kwargs.get('ask_last_date'):
            while not flag:
                if kwargs.get('ask_first_date'):
                    tmp_start_date = input(
                        'Введите начальную дату записи в формате "ГГГГ-ММ-ДД" или оставьте поле пустым: ')
                if kwargs.get('ask_last_date'):
                    tmp_end_date = input(
                        'Введите конечную дату записи в формате "ГГГГ-ММ-ДД" или оставьте поле пустым: ')
                try:
                    if tmp_start_date != '':
                        datetime.date.fromisoformat(tmp_start_date)
                        start_date = tmp_start_date
                    if tmp_end_date != '':
                        datetime.date.fromisoformat(tmp_end_date)
                        end_date = tmp_end_date
                    flag = True
                except ValueError:
                    print('Неверный формат даты. Попробуйте еще раз.')
        while menu_choise != None:
            if not flag:
                menu_choise = self.get_menu_choise(
                    self.records_for_menu(self._nb.select_sheets()))
            else:
                menu_choise = self.get_menu_choise(
                    self.records_for_menu(self._nb.select_sheets(created_first=start_date, created_last=end_date)))
            if menu_choise != None:
                self.show_record(menu_choise)

    def records_for_menu(self, records: dict) -> dict:
        for key in records.keys():
            records[key] = self.timestamp_to_str(
                records[key][0]) + '\t' + records[key][2][:10] + '...'
        return records

    def show_record(self, rec_id: int) -> None:
        sheet = self._nb.select_sheets(ids=[rec_id])
        self.cls()
        print(Fore.WHITE + sheet[rec_id][2] + Fore.RESET + '\n')
        print(sheet[rec_id][3] + '\n')
        menu_items = {1: 'Редактировать', 2: 'Удалить'}
        menu_choise = 0
        while menu_choise != None:
            info_string: str = (f'Дата создания: {self.timestamp_to_str(sheet[rec_id][0])} ' +
                                f'Дата редактирования: {self.timestamp_to_str(sheet[rec_id][1])}').rjust(
                self._width)
            menu_choise = self.get_menu_choise(menu_items,
                                               lambda *args: print(
                                                   Fore.YELLOW + Back.LIGHTBLACK_EX + args[0][0] + Style.RESET_ALL),
                                               False, info_string, donot_cls=True)
            if menu_choise == 1:
                self.add_record(rec_id)
                menu_choise = None
            if menu_choise == 2:
                self.del_record(rec_id)
                menu_choise = None
            if menu_choise != None:
                self.show_record(menu_choise)

    def save_to_csv(self, path: str = '') -> None:
        '''
        Сохраняет блокнот в csv-файл

        Аргументы:
            path: str   - необязательный путь к файлу.
        '''
        if path == '':
            path = input('Введите путь к файлу: ')
        if self._nb.save_csv(path):
            print('Файл успешно записан. Нажмите Enter.')
            self._notebook_path = path
            self.save_cfg()
            input()
        else:
            print('Ошибка записи файла. Нажмите Enter.')
            input()

    def load_from_csv(self, path: str = '') -> None:
        '''
        Загружает блокнот из csv-файла

        Аргументы:
            path: str   - необязательный путь к файлу.
        '''
        if path == '':
            path = input('Введите путь к файлу: ')
        if self._nb.load_csv(path):
            print('Блокнот успешно загужен.')
        else:
            print('Ошибка загрузки блокнота')

    def save_cfg(self) -> None:
        '''
        Сохраняет путь к файлу с последним удачным сохранением, чтобы открыть его снова.
        '''
        try:
            with open(self._cfg, 'w') as cfg_file:
                cfg_file.write(self._notebook_path)
        except EnvironmentError:
            None

    def timestamp_to_str(self, timestamp: float) -> str:
        '''
        Преобразуем timestamp в строку
        '''
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

    def run(self):
        self.main_menu()
