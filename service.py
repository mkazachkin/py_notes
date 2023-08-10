import datetime

_SPLITTER = '\t'


def save_csv(sheets: list, path: str) -> bool:
    '''
    Сохраняет данные из блокнота в csv файл.
    Аргументы:
        sheets: list    - блокнот
        path: str       - путь к файлу
    '''
    if len(sheets) < 2:
        return False
    result: str = ''
    for sheet in sheets:
        result += _SPLITTER. \
            join([escape_str(str(column)) for column in sheet]) + '\n'
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
        return None

    rows: list = csv.split('\n')
    if rows[-1] == '':
        rows.pop()
    if len(rows) < 2:
        return list()
    for i in range(len(rows)):
        rows[i] = rows[i].split(_SPLITTER)
        if len(rows[i]) != 5:
            return list()
        if i != 0:
            try:
                rows[i][0] = int(rows[i][0])
                rows[i][1] = float(rows[i][1])
                rows[i][2] = float(rows[i][2])
            except ValueError:
                return None
        rows[i][3] = escape_str(rows[i][3], True)
        rows[i][4] = escape_str(rows[i][4], True)
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
        '&', '<', '>', '"', "'", '\t', '\n', _SPLITTER]
    _escape_seq: list = [
        '&amp;', '&lt;', '&gt;', '&dquot;', '&squot;', '&tab;', '&br;', '&splitter;']
    _escape_len = len(_escape_chr)
    for i in range(_escape_len):
        if not unescape:
            _result = _result.replace(_escape_chr[i], _escape_seq[i])
        else:
            _result = _result.replace(_escape_seq[i], _escape_chr[i])
    return _result


def timestamp_to_str(timestamp: float) -> str:
    '''
    Преобразуем timestamp в строку
    '''
    return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
