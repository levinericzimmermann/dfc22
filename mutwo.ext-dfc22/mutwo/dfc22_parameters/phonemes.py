__all__ = ("XSAMPAPhoneme",)


class XSAMPAPhoneme(object):
    def __init__(self, phoneme: str):
        self._phoneme = phoneme

    def __str__(self) -> str:
        return self._phoneme

    def __repr__(self) -> str:
        return "XSAMPAPhoneme({self._phoneme})"

    def __hash__(self) -> int:
        return hash(self._phoneme)
