import uuid
import datetime
from model import note


def save_csv(sheets: list[note], path: str) -> bool:
    '''
    Сохраняет данные из блокнота в csv файл.
    Аргументы:
        sheets: list    - блокнот
        path: str       - путь к файлу
    '''
    if len(sheets) == 0:
        return False
    result: str = ''
    result += '\t'.join(sheets[0].get_header()) + '\n'
    for sheet in sheets:
        result += '\t'. \
            join(escape_str(item) for item in sheet.get_list()) + '\n'
    try:
        with open(path, 'w') as csv_file:
            csv_file.write(result)
    except EnvironmentError:
        return False
    return True


def load_csv(path: str) -> list:
    '''
    Считывает данные из файла и вовращает блокнот.
    Возвращает пустой список, если данные загрузить не удалось.

    Аргументы:
        path: str   - путь к файлу
    '''
    try:
        with open(path, 'r') as csv_file:
            csv: str = csv_file.read()
    except EnvironmentError:
        return list()

    rows: list = csv.split('\n')
    for row in rows[1:]:
        note_items = row.split('\t')
        if len(note_items) != 5:
            return list()
        try:
            note_id = uuid.UUID(note_items[0])
            note_created = datetime.datetime.strptime(
                note_items[1], '%Y-%m-%d %H:%M:%S')
            note_modified = datetime.datetime.strptime(
                note_items[2], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return list()
        note_title = escape_str(note_items[3], True)
        note_text = escape_str(note_items[4], True)
        rows.append(note(note_id, note_created,
                    note_modified, note_title, note_text))
    return rows


def escape_str(input_str: str, unescape: bool = False) -> str:
    '''
    Производит экранирование символов и деэкранирование символов в строке.

    Аргументы:
        input_str: str      - входящая строка
        unescape: bool      - направление перевода.
                              True - экранирование, False - деэкраннирование
    '''
    _result: str = input_str
    _escape_chr: list = [
        '&', '<', '>', '"', "'", '\t', '\n']
    _escape_seq: list = [
        '&amp;', '&lt;', '&gt;', '&dquot;', '&squot;', '&tab;', '&br;']
    _escape_len = len(_escape_chr)
    for i in range(_escape_len):
        if not unescape:
            _result = _result.replace(_escape_chr[i], _escape_seq[i])
        else:
            _result = _result.replace(_escape_seq[i], _escape_chr[i])
    return _result
