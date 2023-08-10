from model import sheets
from service import save_csv, load_csv
import datetime


class notebook():
    __slots__ = ['_nb']

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

    def select_sheets(self, **kwargs) -> dict[int, list]:
        '''
        Производит выборку из словаря блокнота по заданным критериям.
        Возвращает новый словарь.

        Аргументы:
            ids: list[int]      - список идентификаторов записей
            created_first: str  - начальная дата создания записи в формате 'ГГГГ-ММ-ДД'
            created_last: str   - конечная дата создания записи в формате 'ГГГГ-ММ-ДД'
        '''
        result = dict(self._nb.sheets)
        if 'ids' in kwargs:
            result = {ids: result[ids]
                      for ids in kwargs.get('ids')
                      if ids in result.keys()}
        flag: bool = False
        first_date: float = 0.0
        last_date: float = datetime.datetime.now().timestamp()
        if 'created_first' in kwargs:
            first_date = datetime.datetime.strptime(
                kwargs.get('created_first'), '%Y-%m-%d').timestamp()
            flag = True
        if 'created_last' in kwargs:
            last_date = datetime.datetime.strptime(kwargs.get(
                'created_last'), '%Y-%m-%d').timestamp() + 86399.9  # 23 часа 59,9 минут
            flag = True
        if flag:
            result = {ids: result[ids] for ids in result.keys() if (
                result[ids][0] >= first_date and result[ids][0] <= last_date)}
        return result

    @property
    def pages(self) -> int:
        '''
        Возвращает количество записей в блокноте
        '''
        return len(self._nb.sheets)

    def load_csv(self, path: str) -> bool:
        '''
        Загружает блокнот из cvs файла.
        В случае успеха возвращает True и заменяет существующий блокнот,
        в противном случае возвращает False, блокнот не изменяется.

        Аргументы:
            path: str       - путь к файлу
        '''
        _nb: list = load_csv(path)
        if _nb != None:
            self._nb = sheets(sheets=self._list_to_nb(_nb))
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
        return save_csv(self._nb_to_list(self._nb), path)

    def _nb_to_list(self, nb: sheets) -> list:
        '''
        Конвертирует словарь блокнота в таблицу с заголовком

        Аргументы:
            nb: sheets  - словарь блокнота
        '''
        result = list()
        result.append(nb.head)
        for rec_id, rec_val in nb.sheets.items():
            result.append(
                [rec_id, rec_val[0], rec_val[1], rec_val[2], rec_val[3]])
        return result

    def _list_to_nb(self, nb: list) -> dict[int, list]:
        '''
        Конвертирует таблицу с заголовком в словарь блокнота

        Аргументы:
            nb: list    - таблица блокнота
        '''
        nb.pop(0)
        return {row[0]: [row[1], row[2], row[3], row[4]] for row in nb}
