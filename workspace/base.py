import abc

class MLModel(abc.ABC):

    @abc.abstractmethod
    def train(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def predict(self, *args, **kwargs):
        pass
