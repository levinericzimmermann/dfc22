from mutwo import dfc22_converters

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

FORCE_TO_COMPUTE_SIMULTANEOUS_UNISONO_EVENT = False

FORCE_TO_COMPUTE_NON_TERMINAL_PAIR_TO_PAGE_COMBINATION_TUPLE = False


del dfc22_converters
