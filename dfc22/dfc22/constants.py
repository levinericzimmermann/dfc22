import itertools

from mutwo import core_utilities
from mutwo import dfc22_converters
from mutwo import dfc22_events
from mutwo import dfc22_parameters

import dfc22


PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS = (
    dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS
)

PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS = (
    dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS
)

VOWEL_TO_JUST_INTONATION_PITCH_DICT = (
    dfc22_events.constants.DEFAULT_VOWEL_TO_JUST_INTONATION_PITCH_DICT
)

CONSONANT_TO_JUST_INTONATION_PITCH_DICT = (
    dfc22_events.constants.DEFAULT_CONSONANT_TO_JUST_INTONATION_PITCH_DICT
)

EXPONENT_TUPLE_TO_CONSONANT_DICT = {
    pitch.exponent_tuple: consonant
    for consonant, pitch in CONSONANT_TO_JUST_INTONATION_PITCH_DICT.items()
}


EXPONENT_TUPLE_TO_VOWEL_DICT = {
    pitch.exponent_tuple: vowel
    for vowel, pitch in VOWEL_TO_JUST_INTONATION_PITCH_DICT.items()
}

NON_TERMINAL_COUNT = len(PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS.non_terminal_tuple)

try:
    assert NON_TERMINAL_COUNT == len(
        PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS.non_terminal_tuple
    )
except AssertionError:
    raise Exception(
        "PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS "
        "and PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS "
        "need to have an equal amount of non terminals."
    )

UNISONO_COUNT = sum(
    [
        len(tuple(itertools.combinations(range(dfc22.configurations.SPEAKER_COUNT), n)))
        for n in range(1, dfc22.configurations.SPEAKER_COUNT + 1)
    ]
)

PAGE_COUNT = int(UNISONO_COUNT // NON_TERMINAL_COUNT)

NON_TERMINAL_PAIR_TO_PAGE_TUPLE = core_utilities.compute_lazy(
    "etc/.pages.pickled",
    force_to_compute=dfc22.configurations.FORCE_TO_COMPUTE_NON_TERMINAL_PAIR_TO_PAGE_TUPLE,
)(
    lambda _, __, exponent_tuple_to_consonant_dict, exponent_tuple_to_vowel_dict, pitch_based_context_free_grammar_for_consonants, pitch_based_context_free_grammar_for_vowels, page_count, word_count: dfc22_converters.PageCountAndWordCountToPageCatalog(
        exponent_tuple_to_consonant_dict,
        exponent_tuple_to_vowel_dict,
        pitch_based_context_free_grammar_for_consonants,
        pitch_based_context_free_grammar_for_vowels,
    ).convert(
        page_count, word_count
    )
)(
    dfc22.configurations.MAX_PAPER_GENERATION_DEPTH,
    dfc22.configurations.MINIMAL_LANGUAGE_STRUCTURE_LENGTH,
    EXPONENT_TUPLE_TO_CONSONANT_DICT,
    EXPONENT_TUPLE_TO_VOWEL_DICT,
    PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS,
    PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS,
    PAGE_COUNT,
    dfc22.configurations.WORD_COUNT,
)

# Cleanup
del dfc22, dfc22_events, dfc22_parameters, itertools
