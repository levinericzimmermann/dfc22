from mutwo import dfc22_parameters
from mutwo import music_parameters


DEFAULT_VOWEL_TO_JUST_INTONATION_PITCH_DICT = {
    dfc22_parameters.XSAMPAPhoneme(vowel): music_parameters.JustIntonationPitch(
        pitch.exponent_tuple
    )
    for vowel, pitch in zip(
        dfc22_parameters.constants.VOWEL_TUPLE,
        dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS.terminal_tuple
        + dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS.non_terminal_tuple,
    )
}


DEFAULT_CONSONANT_TO_JUST_INTONATION_PITCH_DICT = {
    dfc22_parameters.XSAMPAPhoneme(consonant): music_parameters.JustIntonationPitch(
        pitch.exponent_tuple
    )
    for consonant, pitch in zip(
        dfc22_parameters.constants.CONSONANT_TUPLE,
        dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS.terminal_tuple
        + dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS.non_terminal_tuple,
    )
}


DEFAULT_EXPONENT_TUPLE_TO_CONSONANT_DICT = {
    pitch.exponent_tuple: consonant
    for consonant, pitch in DEFAULT_CONSONANT_TO_JUST_INTONATION_PITCH_DICT.items()
}

DEFAULT_EXPONENT_TUPLE_TO_VOWEL_DICT = {
    pitch.exponent_tuple: vowel
    for vowel, pitch in DEFAULT_VOWEL_TO_JUST_INTONATION_PITCH_DICT.items()
}

# Cleanup
del dfc22_parameters, music_parameters
