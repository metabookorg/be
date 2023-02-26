import typing as tp

from .open_ai import GPT3
from .models import *


class TxtCreator:
    def __init__(self, txt_request: BaseTxtRequest | None = None,
                 creativity_risk: float = 0.5
                 ):
        self.request: BaseTxtRequest = txt_request if txt_request else ParamTxtRequest()
        self.creativity_risk: float = creativity_risk


    def create_title(self, text: str) -> str:
        prompt = f"Text:{text}\nTitle:"
        return GPT3.create(text_in=prompt, level=0)

    def create(self) -> str:
        text_in = self.request.get_prompt()
        print(f"\nTEXT IN:\n{text_in}")
        created = GPT3.create(text_in=text_in, creativity_risk=self.creativity_risk)
        print(f"\nCREATED:\n{created}")

        return created


class TxtAnalyzer:
    def __init__(self, text: str):
        self.text: str = text
        self.characters: tp.Dict[str, str] = dict()

    def _characters(self):
        prompt = f"Text:{self.text}\nList characters visual descriptions:"
        raw = GPT3.create(text_in=prompt)
        print(f"RAW CHARACTERS:\n{raw}")
        # TODO: place here replace for each line
        lines = [el for el in raw.split('\n')]
        characters = dict()
        for l in lines:
            splitted = l.split(':')
            if len(splitted) == 2:
                characters[splitted[0]] = splitted[1]
        self.characters = characters

    def analyze(self):
        self._characters()