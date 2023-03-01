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
        return GPT3.create(text_in=prompt, level=0).replace('\n', '').replace('.', '')

    def create(self) -> str:
        text_in = self.request.get_prompt()
        created = GPT3.create(text_in=text_in, creativity_risk=self.creativity_risk)
        print(f"\nCREATED:\n{created}")

        return created


class TxtAnalysis(pdt.BaseModel):
    characters: tp.Dict[str, str]
    sentences: tp.Dict[int, str]
    sentence_characters: tp.Dict[int, tp.List[str]]


class TxtAnalyzer:

    @classmethod
    def _characters(cls, text: str) -> tp.Dict[str, str]:
        prompt = "List characters aspect descriptions.\nExample:\n"
        prompt += "Text:\n"
        prompt += "Rod and Tod start to smoke some weed. "
        prompt += "After a while they began to see some weird creatures and a fairy castle.\n"
        prompt += "Characters:\n"
        prompt += "Rod: A tall, thin teenage boy with shaggy brown hair and bright blue eyes wearing a faded t-shirt and ripped jeans.\n"
        prompt += "Tod: A short, stocky teenage boy with spiky blond hair and dark brown eyes wearing a black hoodie and baggy sweatpants.\n"
        prompt += "Creatures: Strange, alien-like creatures with long, spindly limbs and glowing eyes.\n"
        prompt += f"Text:\n{text}\nCharacters:\n"
        raw = GPT3.create(text_in=prompt).replace('- ', '').replace('-', '')
        # TODO: place here replace for each line
        lines = [el for el in raw.split('\n')]
        characters = dict()
        print(f'DESCRIPTIONS: {lines}')
        for l in lines:
            splitted = l.split(':')
            if len(splitted) == 2:
                name = splitted[0].lower()
                descr = splitted[1].split('.')[0].lower()
                if descr[0] == ' ':
                    descr = descr[1: ]
                characters[name] = descr
        return characters

    @classmethod
    def _sentences(cls, text: str, title: str) -> tp.Dict[int, str]:
        sentences = {0: title.replace('\n', '').replace('.', '')}
        for line in text.replace('\n', '').split('.'):
            if line != '' and len(line) > 4:
                idx = len(sentences)
                sentences[idx] = line.lower()
        return sentences

    @classmethod
    def _sentence_chars(cls, sentences: tp.Dict[int, str]) -> tp.Dict[int, tp.List[str]]:
        prompt = 'For each numbered sentence list all the living characters in it.\n'
        prompt += 'Example:\nSentences:\n'
        prompt += '0. Rod and Tod start to smoke some weed.\n'
        prompt += '1. After a while they began to see some weird creatures and a fairy castle.\n'
        prompt += 'Characters:\n'
        prompt += '0. Rod, Tod\n'
        prompt += '1. Rod, Tod, creatures\n'
        prompt += 'Sentences:\n'
        prompt += '\n'.join([f'{idx}. {line}.' for idx, line in sentences.items()])
        prompt += '.\nCharacters:\n'

        #TODO: DOES NOT WORK ALWAYS
        raw = GPT3.create(text_in=prompt, creativity_risk=0.2)
        lines = [el for el in raw.split('\n')]
        sentence_chars = dict()
        for l in lines:
            splitted = l.split('. ')
            if len(splitted) == 2:
                chars = [el.replace('. ', '').replace('.', '').lower() for el in splitted[1].split(', ') if el != 'None']
                sentence_chars[int(splitted[0])] = chars
        return sentence_chars


    @classmethod
    def analyze(cls, text: str, title: str) -> TxtAnalysis:
        characters = cls._characters(text=text)
        sentences = cls._sentences(text=text, title=title)
        sentence_chars = cls._sentence_chars(sentences=sentences)
        if len(sentences.keys()) != len(sentence_chars.keys()):
            raise Exception(f"Sentences lenght (={len(sentences.keys())} differs from "
                            f"Sentence-characters lenght (={len(sentence_chars.keys())}")
        print('ANALISYS:\n')
        print(f"CHARS:\n{characters}\n")
        print(f"CHARS:\n{sentence_chars}\n")
        return TxtAnalysis(characters=characters, sentences=sentences, sentence_characters=sentence_chars)


class PagePrompt:
    def __init__(self, idx: int, txt: str, prompt: str):
        self.idx: int = int(idx)
        self.txt: str = str(txt)
        self.prompt: str = str(prompt)


class BookPromptsCreator:
    @classmethod
    def get_current_chars(cls, sentence_characters: tp.List[str], chars_descriptions: tp.Dict[str, str]) -> tp.Dict[str, str]:
        selected = dict()
        for name in sentence_characters:
            for long_name, description in chars_descriptions.items():
                if name in long_name:
                    selected[name] = description
        return selected

    @classmethod
    def _create_cover_prompt(cls, title: str) -> PagePrompt:
        return PagePrompt(idx=0, txt=title, prompt=title)

    @classmethod
    def clean_description(cls, description: str) -> str:
        description = description.lower().replace('.', '').replace('illustration:', '')
        description = description.replace('an illustration of ', '').replace('illustration of ', '')
        description = description.replace('an illustration ', '').replace('illustration ', '')
        return description

    @classmethod
    def create(cls, text: str, title: str, style: str) -> tp.List[PagePrompt]:
        analysis = TxtAnalyzer.analyze(text=text, title=title)
        suffix = "Create an illustration description from the text"
        prompt_list = list()
        for idx, line in analysis.sentences.items():
            img_description = GPT3.create(text_in=f"Text:{line}\n{suffix}", creativity_risk=0.0,
                                          one_sentence_mode=True).replace('\n', '')
            img_description = cls.clean_description(description=img_description)
            current_chars = cls.get_current_chars(sentence_characters=analysis.sentence_characters[idx],
                                                  chars_descriptions=analysis.characters)
            prompt = ""
            if style:
                prompt += f"{style.capitalize()} illustration; "
            else:
                prompt += f"An illustration; "
            prompt += f"{img_description}; "
            for name, description in current_chars.items():
                prompt += f"; {name}, {description}"
            prompt_list.append(PagePrompt(idx=idx, txt=line, prompt=prompt))
        return prompt_list


