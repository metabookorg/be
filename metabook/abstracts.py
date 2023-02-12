import abc


class ImageCreator(abc.ABC):

    @abc.abstractmethod
    def create(self, description: str):
        pass

    @abc.abstractmethod
    def manipulate(self, *args, **kwargs):
        pass