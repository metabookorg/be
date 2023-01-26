import typing as tp
import os
from .open_ai import Dalle2
import requests as req


class ImgUrl:
    def __init__(self, name: str, idx: int, url: str):
        self.name: str = name
        self.idx: int = idx
        self.url: str = url


class NaiveImgsCreator:
    _EXTENSION: str = 'png'

    def __init__(self, text: str, title: str):
        self._txt: str = text
        self._title: str = title
        self.images_urls: tp.List[ImgUrl] = list()
        self._folder_path: str = os.path.join(".results", self._title)

    def _split_phrases(self) -> tp.List[str]:
        raw = self._txt
        raw = raw.replace("\n", "").replace("\r", "")
        return raw.split(".")

    def save(self):
        for img_url in self.images_urls:
            try:
                response = req.get(img_url.url)
                if 200 <= response.status_code < 300:
                    with open(os.path.join(self._folder_path, f"{img_url.name}({img_url.idx}).{self._EXTENSION}"), 'wb') as f:
                        f.write(response.content)
            except Exception as e:
                print(f"Exception in saving {img_url.name} image: {e}")
                                
    def create(self):
        splitted = self._split_phrases()
        os.mkdir(os.path.join(".results", self._title))
        for idx, splitted in enumerate(splitted):
            url = Dalle2.create(description=splitted, url_mode=True, n=1)[0]
            self.images_urls.append(ImgUrl(name=splitted, idx=idx, url=url))
        print(f"Pics successfully created.")
