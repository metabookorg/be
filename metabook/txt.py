import typing as tp

from .open_ai import GPT3


class TxtCreator:
    def __init__(self, text_type: str = 'story',
                 argument: str = None,
                 environment: str = None,
                 time: tp.Union[str, list] = None,
                 characters: tp.List[str] = None,
                 creativity_risk: float = 0.5
                 ):
        self.creativity_risk: float = creativity_risk
        self.text_type: str = text_type
        self.argument: str | None = argument
        self.environment: str | None = environment
        self.time: tp.Union[str, list] | None = time
        self.characters: tp.List[str] | None = characters

    def _build_prompt(self):
        text_in = f"Tell me a {self.text_type}"
        if self.argument:
            text_in += f" about {self.argument}"
        if self.environment:
            text_in += f" set in {self.environment}"
        if self.time:
            if isinstance(self.time, list):
                if len(list) == 2:
                    text_in += f" between {self.time[0]} and {self.time[1]}"
                else:
                    text_in += f" in {self.time[0]}"
                    for el in self.time[1:]:
                        text_in += f", {el}"
            else:
                text_in += f" during {self.time}"
        if self.characters:
            text_in += f" with the following characters: {self.characters[0]}"
            for character in self.characters[1:]:
                text_in += f", {character}"
        print(f"PROMPT: {text_in}")
        return text_in

    def create_title(self, text: str) -> str:
        prompt = f"Text:{text}\nTitle:"
        return GPT3.create(text_in=prompt, level=0)

    def create(self) -> str:
        text_in = self._build_prompt()
        print(f"\nTEXT IN:\n{text_in}")
        created = GPT3.create(text_in=text_in, creativity_risk=self.creativity_risk)
        print(f"\nCREATED:\n{created}")
        #corrected = GPT3.edit(text=created, edit="Correct the text grammatically and make it coherent", creativity_risk=0)

        return created


class TxtAnalyzer:
    def __init__(self, text: str):
        self.text: str = text
        self.characters: tp.Dict[str, str] = dict()

    def _characters(self):
        prompt = f"Text:{self.text}\nList characters descriptions:"
        raw = GPT3.create(text_in=prompt)
        # TODO: place here replace for each line
        lines = [el for el in raw.split('\n')]
        characters = dict()
        for l in lines:
            splitted = l.split(':')
            characters[splitted[0]] = splitted[1]
        self.characters = characters

    def analyze(self):
        pass