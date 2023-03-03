import abc
import typing as tp
import os
from .open_ai import Dalle2
import requests as req


from .models import PageUrl, Story
from .txt import BookPromptsCreator
from . import errors as err

class ImgStyles:
    pass

class BaseImgsCreator(abc.ABC):

    def __init__(self, story: Story, style: str = 'comic book'):
        if not isinstance(story, Story):
            raise Exception('story must be instance story')
        self._story: Story = story
        self._style: str = style
        self.images_urls: tp.List[PageUrl] = list()
        self._folder_path: str = os.path.join(".results", self._story.title)

    @abc.abstractmethod
    def save(self):
        pass

    @abc.abstractmethod
    def create(self):
        pass


class ImgsCreator(BaseImgsCreator):
    _EXTENSION: str = 'png'

    def save(self):
        folder = os.path.join("workspace", "results", self._story.title)
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
        page_prompt_list = BookPromptsCreator.create(text=self._story.text, title=self._story.title, style=self._style)
        for page_prompt in page_prompt_list:
            try:
                print(f"TEXT: {page_prompt.prompt}")
                url = Dalle2.create(description=page_prompt.prompt, url_mode=True, n=1)[0]
                print(f"URL: {url}")
                text = page_prompt.txt
                while text[0] == ' ':
                    text = text[1:]
                if page_prompt.idx != 0:
                    text = f"{text.capitalize()}."
                self.images_urls.append(PageUrl(txt=text, idx=page_prompt.idx, url=url))
            except Exception as e:
                print(f"ERROR: {e}")
        print(f"Pics successfully created.")

