"""
Models.
@author: iXB3 (Matteo Causio)
"""

# # Installed
import abc

import pydantic as pdt
import typing as tp

# # Package
from .static import ImgStyle


class BaseModel(pdt.BaseModel):
    "Base model"
    class Config:
        allow_population_by_fields_name = True
        arbitrary_types_allowed = True


class PageUrl(BaseModel):
    txt: str
    idx: int
    url: str


class BaseResponse(BaseModel):
    description: str = "Success"
    data: tp.Union[tp.Dict[str, tp.Any], tp.List[tp.Dict[str, tp.Any]]] | None



class BaseTxtRequest(abc.ABC, BaseModel):
    @abc.abstractmethod
    def get_prompt(self) -> str:
        pass


class PromptTxtRequest(BaseTxtRequest):
    prompt: str

    def get_prompt(self) -> str:
        return self.prompt


class ParamTxtRequest(BaseTxtRequest):
    type: str = 'story'
    argument: str | None
    environment: str | None
    time: tp.Union[str, list] | None
    characters: tp.List[str] | None

    def get_prompt(self) -> str:
        text_in = f"Tell me a {self.type}"
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

class ParamKidBookRequest:
    type: str = 'kids book'


class NewBookRequest(BaseModel):
    """Request of a brand-new book for kids"""
    style: str = ImgStyle.DISNEY_OLD.value
    txt_request: BaseTxtRequest


class NewPromptBookRequest(NewBookRequest):
    txt_request: PromptTxtRequest


class NewKidBookRequest(NewBookRequest):
    """Request of a brand-new book for kids"""
    txt_request: ParamTxtRequest = ParamTxtRequest(type='kids story')


class BookUrlsResponse(BaseResponse):
    data: tp.List[PageUrl]
