from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def transactions(self):
        pass



