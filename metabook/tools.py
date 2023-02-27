"""

"""
# # Installed # #
import typing as tp
import requests as req
from PIL import Image, ImageDraw
from io import BytesIO, StringIO
# # Package # #
from .img import PageUrl



class BookLoader:

    @classmethod
    def add_text(cls, img: Image, text: str):
        draw = ImageDraw.Draw(img)
        draw.text(xy=(0, 0), text=text)

    @classmethod
    def from_urls(cls, book: tp.List[PageUrl], raise_mode: bool = False) -> tp.List[Image.Image]:
        book.sort(key=lambda x: x.idx)
        images = list()
        for img_url in book:
            try:
                response = req.get(img_url.url)
                img = Image.open(BytesIO(response.content))
                cls.add_text(img=img, text=img_url.txt)
                images.append(img)
            except Exception as e:
                if raise_mode:
                    raise e
                print(f"Exception in downloading {img_url.txt} image: {e}")
        return images


class Exporter:
    @classmethod
    def to_pdf(cls, book: tp.List[Image.Image], title: str = None) -> StringIO:
        img_io = StringIO()
        book[0].save(
            img_io, "PDF", resolution=100.0, save_all=True, append_images=book[1:],
            # title="Friendly Title", author="Mark", subject="Friendly Subject"
        )
        img_io.seek(0)

        return img_io

