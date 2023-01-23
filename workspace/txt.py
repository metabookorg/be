import typing as tp

from .open_ai import GPT3


class TxtCreator:
    def __init__(self, text_type: str = 'story',
                 main_argument: str = None,
                 environment: str = None,
                 time: tp.Union[str, list] = None,
                 characters: tp.List[str] = None,
                 creativity_risk: float = 0.5
                 ):
        self.creativity_risk: float = creativity_risk
        self.text_type: str = text_type
        self.main_argument: str | None = main_argument
        self.environment: str | None = environment
        self.time: tp.Union[str, list] | None = time
        self.characters: tp.List[str] | None = characters

    def _build_prompt(self):
        text_in = f"Tell me a {self.text_type}"
        if self.main_argument:
            text_in += f" about {self.main_argument}"
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
        return text_in

    def create(self):
        text_in = self._build_prompt()
        print(f"\nTEXT IN:\n{text_in}")
        created = GPT3.create(text_in=text_in, creativity_risk=self.creativity_risk)
        print(f"\nCREATED:\n{created}")
        #corrected = GPT3.edit(text=created, edit="Correct the text grammatically and make it coherent", creativity_risk=0)

        return created


class TxtAnalyzer:
    def __init__(self, text: str | None):
        self.text: str = text
        self.characters: list = list()
        self.context: str| None = None

    def analyze(self):
        pass