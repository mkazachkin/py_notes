import os
import datetime
from tui.simple_tui import simple_tui
from controller import notebook
from service import timestamp_to_str


class py_notes():
    __slots__ = ['_nb', '_cfg', '_notebook_path', '_tui', '_saved']

    def __init__(self):
        self._tui = simple_tui()
        self._nb = notebook()
        self._cfg = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'main.cfg')
        self._notebook_path = ''
        self._load_cfg()
        self._saved = True
        if self._notebook_path != '':
            self.load_from_csv(self._notebook_path)

    def main_screen(self) -> int:
        '''
        Отображает главное меню
        '''
        menu_items = {
            1: 'Добавить запись',
            2: 'Просмотреть все записи',
            3: 'Просмотреть записи за конкретные даты',
            4: 'Указать путь к csv-файлу и загрузить данные',
            5: 'Указать путь к csv-файлу и сохранить данные',
            6: 'Сохранить',
        }
        # Без match-case, которые появились только в Python 3.11
        menu_choise = 0
        while menu_choise != None:
            if menu_choise == 1:
                self.add_record_screen()
            if menu_choise == 2:
                self.selected_records_screen()
            if menu_choise == 3:
                self.selected_records_screen(
                    ask_first_date=True, ask_last_date=True)
            if menu_choise == 4:
                self.load_from_csv()
            if menu_choise == 5:
                self.save_to_csv()
            if menu_choise == 6:
                self.save_to_csv(self._notebook_path)

            info_str = (f'Текущее количество записей: {self._nb.pages}\n')
            if self._notebook_path != '':
                info_str += f'Файл БД: {self._notebook_path}'
            menu_choise = self._tui.get_menu_choise(menu_items, info_str)

    def selected_records_screen(self, **kwargs) -> None:
        '''
        Выводит список записей.

        Аргументы:
            ask_first_date: bool    - запрос начальной даты
            ask_last_date: bool     - запрос конечной даты
        '''
        flag = False
        start_date = '1970-01-01'
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self._tui.cls()
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
        selected_sheets = dict[int, list]()

        menu_choise = 0
        while menu_choise != None:
            if flag:
                selected_sheets = self._nb.select_sheets(
                    created_first=start_date, created_last=end_date)
            else:
                selected_sheets = self._nb.select_sheets()
            info_str = f'Найдено {len(selected_sheets)} записей'
            menu_items = dict()
            for key in selected_sheets.keys():
                menu_items[key] = timestamp_to_str(
                    selected_sheets[key][0]) + '\t' + selected_sheets[key][2][:10] + '...'
            menu_choise = self._tui.get_menu_choise(menu_items, info_str)
            if menu_choise != None:
                self.record_screen(menu_choise)

    def record_screen(self, rec_id: int) -> None:
        '''
        Отображает содержимое записи

        Аргументы:
            rec_id: int     - идентификатор записи
        '''
        menu_choise = 0
        while menu_choise != None:
            sheet = self._nb.select_sheets(ids=[rec_id])
            self._tui.cls()
            print(sheet[rec_id][2])
            print('-'*self._tui.width)
            print(sheet[rec_id][3])
            print('-'*self._tui.width)
            menu_items = {1: 'Редактировать', 2: 'Удалить'}
            info_string: str = (f'Дата создания: {timestamp_to_str(sheet[rec_id][0])} | ' +
                                f'Дата редактирования: {timestamp_to_str(sheet[rec_id][1])}')
            menu_choise = self._tui.get_menu_choise(
                menu_items, info_string, False, False)
            if menu_choise == 1:
                self.add_record_screen(rec_id)
            elif menu_choise == 2:
                if self.del_record_screen(rec_id):
                    menu_choise = None
            elif menu_choise != None:
                self.record_screen(menu_choise)

    def add_record_screen(self, rec_id: int = -1) -> None:
        '''
        Выводит форму ввода записи и записывает ее в блокнот

        Аргументы:
            rec_id: int     - идентификатор записи, которую нужно заменить
        '''
        self._tui.cls()
        self._tui.print_info(
            'Введите заголовок записи, после чего введите текст записи. Допускается ввод нескольких строк. ' +
            'Для окончания ввода, введите пустую строку. Это очень длинная инструкция, поэтому она должна ' +
            'автоматически разбиться на несколько строк и быть красивой.',
            align='center')
        title: str = input('Заголовок: ')
        print('Текст:')
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
            self._saved = False
        else:
            self._nb.update_sheet(rec_id, title, text)
            self._saved = False

    def del_record_screen(self, rec_id: int) -> bool:
        '''
        Удаляет запись из блокнота. Возвращает информацию о том, была ли запись удалена или нет

        Аргументы:
            rec_id: int     - идентификатор записи
        '''
        flag = self._tui.get_yes_no_menu('Желаете удалить запись?')
        if flag:
            self._nb.remove_sheet(rec_id)
            self._saved = False
        return flag

    def save_to_csv(self, path: str = '') -> None:
        '''
        Сохраняет блокнот в csv-файл

        Аргументы:
            path: str   - необязательный путь к файлу.
        '''
        if path == '':
            path = input('Введите путь к файлу: ')
        if self._nb.save_csv(path):
            self._notebook_path = path
            self._save_cfg()
            self._saved = True
            print('Файл успешно записан. Нажмите Enter.')
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
            self._notebook_path = path
            self._save_cfg()
            self._saved = True
            print('Блокнот успешно загужен.')
        else:
            print('Ошибка загрузки блокнота')
            self._notebook_path = ''
            self._save_cfg()

    def _save_cfg(self) -> None:
        '''
        Сохраняет путь к файлу с последним удачным сохранением, чтобы открыть его снова.
        '''
        try:
            with open(self._cfg, 'w', encoding='utf-8') as cfg_file:
                cfg_file.write(self._notebook_path)
        except EnvironmentError:
            pass

    def _load_cfg(self) -> None:
        '''
        Заргружает путь к файлу с последним удачным сохранением, чтобы открыть его снова.
        '''
        try:
            with open(self._cfg, 'r', encoding='utf-8') as cfg_file:
                self._notebook_path = cfg_file.read()
        except EnvironmentError:
            self._notebook_path = ''
            self._save_cfg()

    def run(self):
        '''
        Запускает текстовый интерфейс приложения и само приложение
        '''
        flag = False
        while not flag:
            self.main_screen()
            flag = self._saved
            if not flag:
                flag = self._tui.get_yes_no_menu(
                    'Записи не сохранены. Все равно выйти?')
