from mutwo import dfc22_events
from mutwo import dfc22_parameters
from mutwo import music_parameters

print("---vowels---")
print(
    "NON-TERMINAL:",
    len(dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS.non_terminal_tuple),
    dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS.non_terminal_tuple,
)
print("")
print(
    "TERMINAL:",
    dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS.terminal_tuple,
)
print("")
# for rule in dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS.context_free_grammar_rule_tuple:
#     print(rule)
# 
# print("")
print(
    "n vowels",
    len(dfc22_events.constants.DEFAULT_EXPONENT_TUPLE_TO_VOWEL_DICT),
    "n items:",
    len(
        dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS.terminal_tuple
    )
    + len(
        dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS.non_terminal_tuple
    ),
)
print("")
for (
    exponent,
    vowel,
) in dfc22_events.constants.DEFAULT_EXPONENT_TUPLE_TO_VOWEL_DICT.items():
    print(music_parameters.JustIntonationPitch(exponent), vowel)

for _ in range(10):
    print("---")

print("---consonants---")
print(
    "NON-TERMINAL:",
    len(dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS.non_terminal_tuple),
    dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS.non_terminal_tuple,
)
print("")
print(
    "TERMINAL:",
    dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS.terminal_tuple,
)
print("")
print(
    "n consonants",
    len(dfc22_events.constants.DEFAULT_EXPONENT_TUPLE_TO_CONSONANT_DICT),
    "n items:",
    len(
        dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS.terminal_tuple
    )
    + len(
        dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS.non_terminal_tuple
    ),
)
print("")
for (
    exponent,
    vowel,
) in dfc22_events.constants.DEFAULT_EXPONENT_TUPLE_TO_CONSONANT_DICT.items():
    print(music_parameters.JustIntonationPitch(exponent), vowel)
