from abc import ABCMeta
from abc import abstractmethod


class ITypeForm(metaclass=ABCMeta):

    @abstractmethod
    def return_html(self, options) -> str:
        pass
