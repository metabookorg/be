import typing as tp

from .open_ai import GPT3
from .models import *

__all__ = (

)


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

class TxtAnalysis(pdt.BaseModel):
    characters: tp.Dict[str, str]

class TxtAnalyzer:
    @classmethod
    def _characters(cls, text: str) -> tp.Dict[str, str]:
        prompt = f"Text:{text}\nList characters visual descriptions:"
        raw = GPT3.create(text_in=prompt)
        print(f"RAW CHARACTERS:\n{raw}")
        # TODO: place here replace for each line
        lines = [el for el in raw.split('\n')]
        characters = dict()
        for l in lines:
            splitted = l.split(':')
            if len(splitted) == 2:
                characters[splitted[0]] = splitted[1]
        return characters

    @classmethod
    def analyze(cls, text: str) -> TxtAnalysis:
        return TxtAnalysis(characters=cls._characters(text=text))

class PagePrompt:
    def __init__(self, idx: int, txt: str, prompt: str):
        self.idx: int = int(idx)
        self.txt: str = str(txt)
        self.prompt: str = str(prompt)


class BookPromptsCreator:
    def get_current_chars(self, sentence: str, characters: tp.Dict[str, str]) -> tp.List[str]:
        selected = list()
        for char in characters.keys():
            if char in sentence:
                selected.append(char)
        return selected

    def create(self, text: str, title: str, style: str) -> tp.List[PagePrompt]:
        analysis = TxtAnalyzer.analyze(text=text)
        sentences = tuple(text.replace('\n', '').split('.'))
        suffix = "Create an illustration description from the text"
        prompt_list = list()
        for idx, line in enumerate(sentences):
            description = GPT3.create(text_in=f"Text:{line}", suffix=suffix, creativity_risk=0.0,
                                      one_sentence_mode=True)
            characters = self.get_current_chars(sentence=line, characters=analysis.characters)
            prompt = ""
            for char in characters:
                prompt += f"{char} {analysis.characters[char]}, "
            prompt = f"{prompt}, {description}, {style} style"
            prompt_list.append(PagePrompt(idx=idx, txt=line, prompt=prompt))
        return prompt_list


