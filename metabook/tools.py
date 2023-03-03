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
        img_width, img_height = img.size
        txt_width, txt_height = draw.textsize(text=text)
        if txt_width > img_width:
            splitted = text.split(' ')
            lines = ['']
            for word in splitted:
                if word:
                    to_check = f"{lines[-1]} {word}"
                    if draw.textsize(text=to_check)[0] < img_width:
                        lines[-1] += f" {word}"
                    else:
                        lines.append(f" {word}")
        else:
            lines = [text]
        draw.text(xy=(1, 0), text='\n'.join(lines))

        #h = 0
        #for idx, l in enumerate(lines):
        #    draw.text(xy=(1, h), text=l)
        #    print(f"h= {h}")
        #    h += draw.textsize(text=l)[1] + 1

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
    def to_pdf(cls, book: tp.List[Image.Image]) -> BytesIO:
        img_io = BytesIO()
        book[0].save(
            img_io, "PDF", resolution=100.0, save_all=True, append_images=book[1:],
            # title="Friendly Title", author="Mark", subject="Friendly Subject"
        )
        img_io.seek(0)

        return img_io

