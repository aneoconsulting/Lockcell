from abc import ABC, abstractmethod


class BaseConfig(ABC):
    def __init__(self, nbRun=None):
        self.nbRun = 1
        if nbRun is not None:
            self.nbRun = nbRun
        self.mode = "default"
        pass

    def setMode(self, mode):
        self.mode = mode

    @abstractmethod
    def Test(self, subspace) -> bool:
        pass

    def setNbRun(self, nbRun):
        self.nbRun = nbRun
        return self

    @abstractmethod
    def copy(self) -> "BaseConfig":
        pass
