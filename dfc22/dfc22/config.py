from mutwo import dfc22_converters

READER_COUNT = SPEAKER_COUNT = 6
"""How many channels / loudspeakers / readers"""

WORD_COUNT = 3
"""How many words for the same Pitch/Rhythm Movement"""

dfc22_converters.constants.DEFAULT_LIMIT = MAX_PAPER_GENERATION_DEPTH = 6
"""Higher = better quality (less repetitions) = longer calculation times"""

FORCE_TO_COMPUTE_NON_TERMINAL_PAIR_TO_PAGE_TUPLE = False


del dfc22_converters
