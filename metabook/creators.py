import typing as tp

from .txt import TxtCreator, TxtAnalyzer
from .img import ImgsCreator, NaiveImgsCreator, PageUrl
from .static import ImgStyle


class BookCreator:
    def __init__(self, txt_creator: TxtCreator = TxtCreator(),
                 imgs_creator_class: tp.Type[ImgsCreator] = NaiveImgsCreator):
        self.txt_creator: TxtCreator = txt_creator
        self.imgs_creator_class: tp.Type[ImgsCreator] = imgs_creator_class
        self.imgs_creator: ImgsCreator | None = None

    def save(self):
        self.imgs_creator.save()

    def create(self, save: bool = False, title: str = None, text: str = None,
               style: str = ImgStyle.CYBERPUNK.value) -> tp.List[PageUrl]:
        if not text:
            text = self.txt_creator.create()
        if not title:
            title = self.txt_creator.create_title(text=text)
            print(f"\nTITLE:\n{title}")

        self.imgs_creator = self.imgs_creator_class(title=title, text=text, style=style)
        self.imgs_creator.create()
        if save:
            self.save()
        return self.imgs_creator.images_urls

