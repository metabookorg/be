import typing as tp

from .txt import TxtCreator
from .img import BaseImgsCreator, ImgsCreator, PageUrl
from .static import ImgStyle
from .models import Story


class BookCreator:
    def __init__(self, txt_creator: TxtCreator = TxtCreator(),
                 imgs_creator_class: tp.Type[BaseImgsCreator] = ImgsCreator):
        self.txt_creator: TxtCreator = txt_creator
        self.imgs_creator_class: tp.Type[BaseImgsCreator] = imgs_creator_class
        self.imgs_creator: BaseImgsCreator | None = None

    def save(self):
        self.imgs_creator.save()

    def create(self, save: bool = False, story: Story | None = None,
               style: str = ImgStyle.CYBERPUNK.value) -> tp.List[PageUrl]:
        if not isinstance(story, Story):
            story = self.txt_creator.create()

        self.imgs_creator = self.imgs_creator_class(story=story, style=style)
        self.imgs_creator.create()
        if save:
            self.save()
        return self.imgs_creator.images_urls

