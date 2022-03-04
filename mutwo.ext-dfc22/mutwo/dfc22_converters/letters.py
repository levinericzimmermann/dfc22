from mutwo import core_converters
from mutwo import dfc22_events
from mutwo import dfc22_parameters


__all__ = ("WordToLetterTuple", "SentenceToLetterTuple")


class WordToLetterTuple(core_converters.abc.Converter):
    def __init__(self, alphabet: dfc22_parameters.Alphabet):
        self._alphabet = alphabet

    def convert(
        self, word_to_convert: dfc22_events.Word
    ) -> tuple[dfc22_parameters.Letter, ...]:
        letter_list = []
        for phoneme_group in word_to_convert:
            for phoneme in phoneme_group.phoneme_list:
                letter_list.append(self._alphabet.get_letter_tuple(phoneme)[0])
        return tuple(letter_list)


class SentenceToLetterTuple(core_converters.abc.Converter):
    def __init__(self, word_to_letter_tuple: WordToLetterTuple):
        self._word_to_letter_tuple = word_to_letter_tuple

    def convert(
        self, sentence_to_convert: tuple[dfc22_events.Word, ...]
    ) -> tuple[dfc22_parameters.Letter, ...]:
        letter_list = []
        for word in sentence_to_convert:
            letter_list.extend(self._word_to_letter_tuple(word))
            letter_list.extend(
                self._word_to_letter_tuple._alphabet.get_letter_tuple(
                    dfc22_parameters.XSAMPAPhoneme("_")
                )
            )
            letter_list.extend(
                self._word_to_letter_tuple._alphabet.get_letter_tuple(
                    dfc22_parameters.XSAMPAPhoneme("_")
                )
            )
        letter_list.extend(
            self._word_to_letter_tuple._alphabet.get_letter_tuple(
                dfc22_parameters.XSAMPAPhoneme("_")
            )
        )
        letter_list.extend(
            self._word_to_letter_tuple._alphabet.get_letter_tuple(
                dfc22_parameters.XSAMPAPhoneme("_")
            )
        )
        return tuple(letter_list)
