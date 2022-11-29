import abc
import numpy as np
from PIL import Image


class BaseLoader(abc.ABC):
    @abc.abstractmethod
    def upload(self, file: str) -> np.ndarray:
        pass

    @abc.abstractmethod
    def download(self, data: np.array, file: str):
        pass


class ImgLoader(BaseLoader):
    def upload(self, file: str) -> np.ndarray:
        # load the image and convert into
        # numpy array
        img = Image.open(file)

        # asarray() class is used to convert
        # PIL images into NumPy arrays
        np_img = np.array(img)
        return np_img

    def download(self, data: np.ndarray, file: str):
        # Below is the way of creating Pillow
        # image from our numpyarray
        img = Image.fromarray(data)
        img.save(fp=file)



class VidLoader(BaseLoader):
    def upload(self, file: str) -> np.ndarray:
        pass

    def download(self, data: np.ndarray, file: str):
        pass
