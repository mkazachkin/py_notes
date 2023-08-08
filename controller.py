from model import sheets
from service import save_csv, load_csv
import datetime


class notebook():
    __slots__ = ['_sheets']

    def __init__(self) -> None:
        '''
        Класс блокнота.
        '''
        self._nb: sheets = sheets()

    def add_sheet(self, title: str, text: str) -> None:
        '''
        Добавляет запись
        '''
        self._nb.add(title, text)

    def update_sheet(self, id: int, title: str, text: str) -> None:
        '''
        Изменяет запись по id.
        '''
        self._nb.mod(id, title, text)

    def remove_sheet(self, id: int) -> None:
        '''
        Удаляет запись по id.
        '''
        self._nb.rem(id)

    def select_sheets(self, **kwargs) -> dict:
        result = dict(self._nb)
        if 'ids' in kwargs:
            result = {ids: result[ids]
                      for ids in kwargs.get('ids')
                      if ids in result.keys()}
        flag: bool = False
        first_date: float = 0.0
        last_date: float = datetime.datetime.now().timestamp()
        if 'created_first' in kwargs:
            try:
                first_date = datetime.datetime.\
                    strptime(kwargs.get('created_first'),
                             '%Y-%m-%d').timestamp()
                flag = True
            except ValueError:
                return dict()
        if 'created_last' in kwargs:
            try:
                last_date = datetime.datetime.\
                    strptime(kwargs.get('created_last'),
                             '%Y-%m-%d').timestamp()
                flag = True
            except ValueError:
                return dict()
        if flag:
            result = {ids: result[ids]
                      for ids in result.keys()
                      if result[ids][0] >= first_date
                      and result[ids][0] <= last_date}
        return result

    def load_csv(self, path: str) -> bool:
        '''
        Загружает блокнот из cvs файла.
        В случае успеха возвращает True и заменяет существующий блокнот,
        в противном случае возвращает False, блокнот не изменяется.

        Аргументы:
            path: str       - путь к файлу
        '''
        tmp_sheets = load_csv(path)
        if len(tmp_sheets) != 0:
            self._sheets = tmp_sheets
            return True
        else:
            return False

    def save_csv(self, path: str) -> bool:
        '''
        Загружает блокнот из cvs файла.
        В случае успеха возвращает True, в противном случае возвращает False.

        Аргументы:
            path: str       - путь к файлу
        '''
        return save_csv(self._sheets, path)
