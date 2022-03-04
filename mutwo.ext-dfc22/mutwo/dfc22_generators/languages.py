import itertools

import numpy as np

from mutwo import common_generators
from mutwo import dfc22_events
from mutwo import dfc22_parameters
from mutwo import zimmermann_generators


__all__ = ("make_word_tuple", "SentenceGenerator")


def make_word_tuple(
    consonant_start: zimmermann_generators.JustIntonationPitchNonTerminal,
    consonant_length: int,
    vowel_start: zimmermann_generators.JustIntonationPitchNonTerminal,
    vowel_length: int,
) -> tuple[dfc22_events.Word, ...]:

    if consonant_length:
        consonant_resolution = dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS.resolve(
            consonant_start, consonant_length - 1
        )
        consonant_leaf_tuple = tuple(
            leaf.data
            for leaf in consonant_resolution.leaves()
            if len(leaf.data) == consonant_length
        )
    else:
        consonant_leaf_tuple = tuple([[]])

    if vowel_length:
        vowel_resolution = dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS.resolve(
            vowel_start, vowel_length - 1
        )
        vowel_leaf_tuple = tuple(
            leaf.data
            for leaf in vowel_resolution.leaves()
            if len(leaf.data) == vowel_length
        )
    else:
        vowel_leaf_tuple = tuple([[]])

    word_list = []

    for consonant_data, vowel_data in itertools.product(
        consonant_leaf_tuple, vowel_leaf_tuple
    ):

        consonant_iterator, vowel_iterator = iter(consonant_data), iter(vowel_data)
        length_tuple = (len(consonant_data), len(vowel_data))
        euclidean_distribution = common_generators.euclidean(max(length_tuple), sum(length_tuple))
        # vowel is always == 1
        # consonant is always == 0
        if length_tuple[0] > length_tuple[1]:
            euclidean_distribution = tuple(
                int(not value) for value in euclidean_distribution
            )
        word = dfc22_events.Word([])
        for value in euclidean_distribution:
            if value:
                current_vowel = next(vowel_iterator)
                phoneme = dfc22_events.constants.DEFAULT_EXPONENT_TUPLE_TO_VOWEL_DICT[
                    current_vowel.exponent_tuple
                ]
            else:
                current_consonant = next(consonant_iterator)
                phoneme = (
                    dfc22_events.constants.DEFAULT_EXPONENT_TUPLE_TO_CONSONANT_DICT[
                        current_consonant.exponent_tuple
                    ]
                )
            phoneme_group = dfc22_events.PhonemeGroup(phoneme_list=[phoneme])
            word.append(phoneme_group)

        word_list.append(word)

    return tuple(word_list)


class SentenceGenerator(object):
    def __init__(self, *word_tuple: tuple[dfc22_events.Word], seed=10):
        self._word_tuple_tuple = word_tuple
        self._random = np.random.default_rng(seed)

    def __next__(self) -> tuple[dfc22_events.Word, ...]:
        word_list = []
        for word_tuple in self._word_tuple_tuple:
            choosen_word = dfc22_events.Word(self._random.choice(word_tuple, 1)[0])
            word_list.append(choosen_word)
        return tuple(word_list)
