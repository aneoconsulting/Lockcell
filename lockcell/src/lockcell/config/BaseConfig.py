from abc import ABC, abstractmethod
from typing import Optional


class BaseConfig(ABC):
    def __init__(self, nbRun: Optional[int] = None):
        self.nbRun = 1
        if nbRun is not None:
            self.nbRun = nbRun
        self.mode = "default"
        pass

    def set_mode(self, mode):
        self.mode = mode

    @abstractmethod
    def test_(self, subspace) -> bool:
        pass

    @abstractmethod
    def generate_search_space(self) -> list:
        pass

    def set_nb_run(self, nbRun):
        self.nbRun = nbRun
        return self

    @abstractmethod
    def __copy__(self) -> "BaseConfig":
        raise NotImplementedError("Cannot copy the abstract class BaseConfig")
