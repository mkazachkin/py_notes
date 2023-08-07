import note
import pandas as pd


class notebook (note):
    def __init__(self, **kwargs) -> None:
        self._df = pd.DataFrame(columns=['id', 'date_creation', 'date_change', 'title', 'text'])
