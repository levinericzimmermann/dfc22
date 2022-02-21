from PIL import Image

from mutwo import dfc22_parameters

__all__ = ("SignElement", "SignGrid", "PhonemeList")

PhonemeList = list[list[dfc22_parameters.XSAMPAPhoneme]]


class SignElement(dfc22_parameters.abc.Sign):
    def __init__(
        self,
        image: Image.Image,
        phoneme_list: PhonemeList,
    ):
        self._image = image
        self._phoneme_list = phoneme_list

    @property
    def image(self) -> Image.Image:
        return self._image

    @property
    def phoneme_list(self) -> PhonemeList:
        return self._phoneme_list


class SignGrid(dfc22_parameters.abc.Sign):
    pass
