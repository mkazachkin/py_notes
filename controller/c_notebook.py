class c_notebook():
    def __init__(self) -> None:
        self._escape_chr: list = [
            '&', '<', '>', '"', "'", '\t', '\n']
        self._escape_seq: list = [
            '&amp;', '&lt;', '&gt;', '&quot;', '&#x27;', '&nbsp;&nbsp;&nbsp;&nbsp;', '<br>']
        self._escape_len = len(self._escape_chr)
        self._dt.set_index = ('id')