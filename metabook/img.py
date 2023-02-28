import abc
import typing as tp
import os
from .open_ai import Dalle2
import requests as req

from .models import PageUrl
from .txt import BookPromptsCreator

class ImgStyles:
    pass

class ImgsCreator(abc.ABC):

    def __init__(self, text: str, title: str, style: str = 'comic book'):
        self._txt: str = text
        self._title: str = title
        self._style: str = style
        self.images_urls: tp.List[PageUrl] = list()
        self._folder_path: str = os.path.join(".results", self._title)

    @abc.abstractmethod
    def save(self):
        pass

    @abc.abstractmethod
    def create(self):
        pass


class NaiveImgsCreator(ImgsCreator):
    _EXTENSION: str = 'png'

    def _split_phrases(self) -> tp.List[str]:
        raw = self._txt
        raw = raw.replace("\n", "").replace("\r", "")
        return raw.split(".")

    def save(self):
        folder = os.path.join("workspace", "results", self._title)
        os.makedirs(folder)
        for img_url in self.images_urls:
            try:
                response = req.get(img_url.url)
                if 200 <= response.status_code < 300:
                    with open(os.path.join(self._folder_path, f"{img_url.idx}-{img_url.txt}.{self._EXTENSION}"), 'wb') as f:
                        f.write(response.content)
            except Exception as e:
                print(f"Exception in saving {img_url.txt} image: {e}")

    def create(self):
        page_prompt_list = BookPromptsCreator.create(text=self._txt, title=self._title, style=self._style)
        for page_prompt in page_prompt_list:
            try:
                print(f"TEXT: {page_prompt.prompt}")
                url = Dalle2.create(description=page_prompt.prompt, url_mode=True, n=1)[0]
                print(f"URL: {url}")
                self.images_urls.append(PageUrl(txt=page_prompt.txt, idx=page_prompt.idx, url=url))
            except Exception as e:
                print(f"ERROR: {e}")
        print(f"Pics successfully created.")

