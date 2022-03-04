import typing

from mutwo import isis_converters

__all__ = ("XSAMPAPhoneme",)


class XSAMPAPhoneme(object):
    def __init__(self, phoneme: str):
        self._phoneme = phoneme

    def __str__(self) -> str:
        return self._phoneme

    def __repr__(self) -> str:
        return f"XSAMPAPhoneme({self._phoneme})"

    def __hash__(self) -> int:
        return hash(self._phoneme)

    def __eq__(self, other: typing.Any) -> bool:
        try:
            return hash(self) == hash(other)
        except TypeError:
            return False

    @property
    def phoneme(self) -> str:
        return self._phoneme

    @property
    def is_vowel(self) -> bool:
        return str(self) in isis_converters.constants.XSAMPA.vowel_tuple

    @property
    def is_consonant(self) -> bool:
        return not self.is_vowel
