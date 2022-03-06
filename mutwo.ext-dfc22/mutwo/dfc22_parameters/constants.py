from mutwo import isis_converters
from mutwo import zimmermann_generators

XSAMPA_VOWEL_TO_FORMANT_FREQUENCY_TUPLE_DICT = {
    # formant (xsampa notation): (f0, f1)
    "i": (240, 2400),
    "y": (235, 2100),
    "e": (390, 2300),
    "2": (370, 1900),
    "E": (610, 1900),
    "9": (585, 1710),
    "a": (850, 1610),
    "&": (820, 1530),
    "A": (750, 940),
    "Q": (700, 760),
    "V": (600, 1170),
    "O": (500, 700),
    "7": (460, 1310),
    "o": (360, 640),
    "M": (300, 1390),
    "u": (250, 595),
    # different reference!
    "@": (665, 1772),
}
"""Average vowel formants for a male voice.

Except for '@' all vowels are based on the following reference:

Catford, J.C. (1988) A Practical Introduction to Phonetics,
Oxford University Press, p. 161. ISBN 978-0198242178.

The frequencies of '@' are based on the paper
'The phonetics of schwa vowels' written by
Edward Flemming.
"""

VOWEL_TUPLE = isis_converters.constants.XSAMPA.vowel_tuple

CONSONANT_TUPLE = (
    isis_converters.constants.XSAMPA.semi_vowel_tuple
    + isis_converters.constants.XSAMPA.voiced_fricative_tuple
    + isis_converters.constants.XSAMPA.unvoiced_fricative_tuple
    + isis_converters.constants.XSAMPA.voiced_plosive_tuple
    + isis_converters.constants.XSAMPA.unvoiced_plosive_tuple
    + isis_converters.constants.XSAMPA.nasal_tuple
    + isis_converters.constants.XSAMPA.other_tuple
)

DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS = (
    zimmermann_generators.PitchBasedContextFreeGrammar.from_constraints(
        prime_number_to_maximum_exponent_dict={3: 2, 7: 1, 11: 1},
        maximum_cent_deviation=450,
        minimal_barlow_harmonicity_non_terminal=0.05,
        minimal_barlow_harmonicity_terminal=0.04,
        add_unison=True,
    )
)

DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS = zimmermann_generators.PitchBasedContextFreeGrammar.from_constraints(
    # prime_number_to_maximum_exponent_dict={3: 3, 7: 1, 11: 1},
    prime_number_to_maximum_exponent_dict={3: 1, 5: 1, 7: 1},
    maximum_cent_deviation=1200,
    minimal_barlow_harmonicity_non_terminal=0.115,
    # minimal_barlow_harmonicity_terminal=0.037,
    minimal_barlow_harmonicity_terminal=0.083,
    add_unison=True,
    allowed_octave_sequence=(-1, 0, 1),
)


del isis_converters, zimmermann_generators
