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
    text: str
    characters: tp.Dict[str, str]
    sentences: tp.Dict[int, str]
    sentence_characters: tp.Dict[int, tp.List[str]]


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
    def _sentences(cls, text: str) -> tp.Dict[int, str]:
        return {idx: splitted for idx, splitted in enumerate(text.replace('\n', '').split('.'))}

    @classmethod
    def _sentence_chars(cls, sentences: tp.Dict[int, str]) -> tp.Dict[int, tp.List[str]]:
        prompt = '.\n'.join([f'{idx}. {line}' for idx, line in sentences.items()]) + '.\n'
        suffix = 'For each numbered sentence list all the characters in it.'
        raw = GPT3.create(text_in=prompt, suffix=suffix, creativity_risk=0.2)
        lines = [el for el in raw.split('\n')]
        sentence_chars = dict()
        for l in lines:
            splitted = l.split('. ')
            if len(splitted) == 2:
                chars = [el for el in splitted[1].split(', ') if el != 'None']
                sentence_chars[int(splitted[0])] = chars
        return sentence_chars


    @classmethod
    def analyze(cls, text: str) -> TxtAnalysis:
        characters = cls._characters(text=text)
        sentences = cls._sentences(text=text)
        sentence_chars = cls._sentence_chars(sentences=sentences)
        if len(sentences.keys()) != len(sentence_chars.keys()):
            raise Exception(f"Sentences lenght (={len(sentences.keys())} differs from "
                            f"Sentence-characters lenght (={len(sentence_chars.keys())}")
        return TxtAnalysis(characters=characters, sentences=sentences, sentence_chars=sentence_chars)

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

    def _create_cover_prompt(self, title: str) -> PagePrompt:
        return PagePrompt(idx=0, txt=title, prompt=title)

    def create(self, text: str, title: str, style: str) -> tp.List[PagePrompt]:
        analysis = TxtAnalyzer.analyze(text=text)
        suffix = "Create an illustration description from the text"
        prompt_list = list()
        # TODO: ADD COVER WITH TITLE
        prompt_list.append(self._create_cover_prompt(title=title))
        for idx, line in analysis.sentences.items():
            description = GPT3.create(text_in=f"Text:{line}", suffix=suffix, creativity_risk=0.0,
                                      one_sentence_mode=True)
            characters = [char for char in analysis.sentence_characters[idx] if char in analysis.characters.keys()]
            prompt = ""
            for char in characters:
                prompt += f"{char} {analysis.characters[char]}, "
            prompt = f"{prompt}, {description}, {style} style"
            prompt_list.append(PagePrompt(idx=idx + 1, txt=line, prompt=prompt))
        return prompt_list


