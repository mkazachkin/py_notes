from model import note
from service import save_csv, load_csv


class sheets():
    __slots__ = ['_sheets']

    def __init__(self, **kwargs) -> None:
        '''
        Класс блокнота.

        Аргументы конструктора:
            sheets: note    - список записей
        '''
        self._sheets: list[note] = kwargs.get('sheets', list())

    def push(self, text_note: note) -> None:
        '''
        Добавляет запись
        '''
        self._sheets.append(text_note)

    def pop(self, idx=-1) -> note:
        '''
        Удаляет и возвращает запись по указанному индексу. По-умочанию, последнюю.
        '''
        return self._sheets.pop(idx)

    def get(self, idx=-1) -> note:
        '''
        Возвращает запись по указанному индексу. По-умолчанию, последнюю.
        '''
        return self._sheets[idx]

    def get_all(self) -> list[note]:
        '''
        Возвращает все записи блокнота
        '''
        return self._sheets

    def clear(self):
        '''
        Очищает блокнот.
        '''
        self._sheets.clear()

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

    def load_json(path: str) -> None:
        None

    def save_json(path: str) -> None:
        None

    def records_num(self) -> bool:
        '''
        Возвращает True, если блокнот пустой.
        '''
        return len(self._sheets)
