from mutwo import dfc22_converters
from mutwo import dfc22_events
from mutwo import dfc22_parameters
from mutwo import zimmermann_generators

READER_COUNT = READER_COUNT = 6
"""How many channels / loudspeakers / readers"""

SEQUENTIAL_UNISONO_EVENT_REPEAT_COUNT = 2
"""How often the same sequential unisono event shall be repeated"""

WORD_COUNT = 2
"""How many words for the same Pitch/Rhythm Movement"""

MIN_READER_COMBINATION_COUNT = 2
"""How many readers are minimally combined for am unisono part"""

MAX_READER_COMBINATION_COUNT = 3
"""How many readers are maximally combined for an unisono part"""

dfc22_converters.configurations.DEFAULT_LIMIT = MAX_PAPER_GENERATION_DEPTH = 8
"""Higher = better quality (less repetitions) = longer calculation times"""

MAX_PAPER_SIDE_GENERATION_DEPTH = 5
"""Higher = better quality (less repetitions) = longer calculation times"""

dfc22_converters.configurations.DEFAULT_MINIMAL_RESOLUTION_LENGHT = (
    MINIMAL_LANGUAGE_STRUCTURE_LENGTH
) = 3
"""Higher = longer papers"""

dfc22_converters.configurations.DEFAULT_MAXIMUM_PAGE_COMBINATION_COUNT = (
    MAXIMUM_PAGE_COMBINATION_COUNT
) = 3
"""Higher = more complex and longer interpolations between two unisono parts"""

dfc22_converters.configurations.DEFAULT_MINIMAL_PAGE_COMBINATION_COUNT = (
    MINIMAL_PAGE_COMBINATION_COUNT
) = 390
"""Higher = fewer options to find fixed points of unisono parts (more
options when picking the actual movements == hopefully more harmonic
result)"""

FORCE_TO_COMPUTE_NON_TERMINAL_PAIR_TO_PAGE_TUPLE = False

FORCE_TO_COMPUTE_NON_TERMINAL_PAIR_PER_SEQUENTIAL_UNISONO_EVENT = False

FORCE_TO_COMPUTE_SIMULTANEOUS_EVENT_WITH_PAGES = False

FORCE_TO_COMPUTE_SIMULTANEOUS_EVENT_WITH_NOTES = False

FORCE_TO_COMPUTE_SIMULTANEOUS_EVENT_WITH_NOTES_FOR_ISIS = False

FORCE_TO_COMPUTE_NON_TERMINAL_PAIR_TO_PAGE_COMBINATION_TUPLE = False

PITCH_OFFSET = zimmermann_generators.JustIntonationPitchNonTerminal("1/1")

RHYTHM_OFFSET = zimmermann_generators.JustIntonationPitchNonTerminal("1/8")

dfc22_converters.configurations.PAGE_BUFFER_DURATION = 3
"""longer -> longer rests between pages"""

dfc22_events.configurations.DEFAULT_UNCERTAIN_DURATION_FOR_PHONEME_GROUP = (
    dfc22_parameters.UncertainRange(0.1, 0.195)
)
# https://www.researchgate.net/figure/The-average-duration-of-phonemes_tbl1_352355866
# https://www.asel.udel.edu/icslp/cdrom/vol4/301/a301.pdf

dfc22_events.configurations.DEFAULT_UNCERTAIN_REST_DURATION_FOR_PHONEME_GROUP = (
    dfc22_parameters.UncertainRange(0.04, 0.08)
)

dfc22_events.configurations.DEFAULT_UNCERTAIN_REST_DURATION_FOR_WORD = (
    dfc22_parameters.UncertainRange(0.1, 0.3)
)

dfc22_events.configurations.DEFAULT_UNCERTAIN_REST_DURATION_FOR_SENTENCE = (
    dfc22_parameters.UncertainRange(0.4, 1)
)

dfc22_events.configurations.DEFAULT_UNCERTAIN_REST_DURATION_FOR_PARAGRAPH = (
    dfc22_parameters.UncertainRange(1.5, 2.5)
)

dfc22_events.configurations.DEFAULT_UNCERTAIN_REST_DURATION_FOR_PAGE = (
    dfc22_parameters.UncertainRange(3, 8)
)


del dfc22_converters, dfc22_parameters, zimmermann_generators
