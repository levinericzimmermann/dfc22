import abc

from PIL import Image

from mutwo import dfc22_parameters

__all__ = ("Sign",)


class Sign(abc.ABC):
    @property
    @abc.abstractmethod
    def image(self) -> Image.Image:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def phoneme_list(self) -> list[list[dfc22_parameters.XSAMPAPhoneme]]:
        raise NotImplementedError


# Cleanup module
del abc
