import typing as tp
import os
from .open_ai import Dalle2


class NaiveImgsCreator:
    _EXTENSION: str = 'jpeg'

    def __init__(self, text: str, title: str):
        self._txt: str = text
        self._title: str = title

    def _split_phrases(self) -> tp.List[str]:
        raw = self._txt
        raw = raw.replace("\n", "").replace("\r", "")
        return raw.split(".")

    def create(self):
        splitted = self._split_phrases()
        os.mkdir(os.path.join(".results", self._title))
        for idx, splitted in enumerate(splitted):
            with os.open(os.path.join(".results", self._title, f"{str(idx)}.{self._EXTENSION}")) as f:
                f.save(Dalle2.create(description=splitted))
        print(f"Pics successfully created.")
