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

SEQUENTIAL_UNISONO_EVENT = dfc22_converters.ReaderCountToSequentialUnisonoEvent(
    dfc22.configurations.MIN_READER_COMBINATION_COUNT,
    dfc22.configurations.MAX_READER_COMBINATION_COUNT,
).convert(dfc22.configurations.READER_COUNT)

for _ in range(dfc22.configurations.SEQUENTIAL_UNISONO_EVENT_REPEAT_COUNT - 1):
    SEQUENTIAL_UNISONO_EVENT.extend(SEQUENTIAL_UNISONO_EVENT)

UNISONO_COUNT = len(SEQUENTIAL_UNISONO_EVENT)

PAGE_COUNT = int(UNISONO_COUNT // NON_TERMINAL_COUNT)

NON_TERMINAL_PAIR_TO_PAGE_TUPLE = core_utilities.compute_lazy(
    "etc/.pages.pickled",
    force_to_compute=dfc22.configurations.FORCE_TO_COMPUTE_NON_TERMINAL_PAIR_TO_PAGE_TUPLE,
)(
    lambda _, __, ___, ____, _____: dfc22_converters.PageCountAndWordCountToPageCatalog(
        EXPONENT_TUPLE_TO_CONSONANT_DICT,
        EXPONENT_TUPLE_TO_VOWEL_DICT,
        PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS,
        PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS,
        dfc22.configurations.MAX_PAPER_SIDE_GENERATION_DEPTH,
    ).convert(PAGE_COUNT, dfc22.configurations.WORD_COUNT)
)(
    dfc22.configurations.MAX_PAPER_GENERATION_DEPTH,
    dfc22.configurations.MINIMAL_LANGUAGE_STRUCTURE_LENGTH,
    dfc22.configurations.MIN_READER_COMBINATION_COUNT,
    dfc22.configurations.MAX_READER_COMBINATION_COUNT,
    dfc22.configurations.SEQUENTIAL_UNISONO_EVENT_REPEAT_COUNT,
)

NON_TERMINAL_PAIR_TO_PAGE_COMBINATION_TUPLE = core_utilities.compute_lazy(
    "etc/.non_terminal_pair_to_page_combination_tuple.pickled",
    force_to_compute=dfc22.configurations.FORCE_TO_COMPUTE_NON_TERMINAL_PAIR_TO_PAGE_COMBINATION_TUPLE,
)(
    lambda _, __, ___, ____, ______, _______, ________: dfc22_converters.PageCatalogToPageCombinationCatalog().convert(
        NON_TERMINAL_PAIR_TO_PAGE_TUPLE
    )
)(
    dfc22.configurations.MAX_PAPER_GENERATION_DEPTH,
    dfc22.configurations.MINIMAL_LANGUAGE_STRUCTURE_LENGTH,
    dfc22.configurations.MINIMAL_PAGE_COMBINATION_COUNT,
    dfc22.configurations.MAXIMUM_PAGE_COMBINATION_COUNT,
    dfc22.configurations.MIN_READER_COMBINATION_COUNT,
    dfc22.configurations.MAX_READER_COMBINATION_COUNT,
    dfc22.configurations.SEQUENTIAL_UNISONO_EVENT_REPEAT_COUNT,
)


PAGE_PER_SEQUENTIAL_UNISONO_EVENT = dfc22_converters.SequentialUnisonoEventToPageTuple(
    NON_TERMINAL_PAIR_TO_PAGE_TUPLE
).convert(SEQUENTIAL_UNISONO_EVENT)

from mutwo import music_parameters

vowel, consonant = (
    music_parameters.JustIntonationPitch(),
    music_parameters.JustIntonationPitch(),
)

[
    unisono_event.set_parameter("page", non_terminal_pair)
    for unisono_event, non_terminal_pair in zip(
        SEQUENTIAL_UNISONO_EVENT, PAGE_PER_SEQUENTIAL_UNISONO_EVENT
    )
]


NON_TERMINAL_PAIR_PER_SEQUENTIAL_UNISONO_EVENT = core_utilities.compute_lazy(
    "etc/.non_terminal_pair_per_sequential_unisono_event.pickled",
    force_to_compute=dfc22.configurations.FORCE_TO_COMPUTE_NON_TERMINAL_PAIR_PER_SEQUENTIAL_UNISONO_EVENT,
)(
    lambda _, __, ___: dfc22_converters.SequentialUnisonoEventToNonTerminalPairTuple(
        NON_TERMINAL_PAIR_TO_PAGE_COMBINATION_TUPLE
    ).convert(SEQUENTIAL_UNISONO_EVENT)
)(
    SEQUENTIAL_UNISONO_EVENT,
    dfc22.configurations.MAX_PAPER_GENERATION_DEPTH,
    dfc22.configurations.MINIMAL_LANGUAGE_STRUCTURE_LENGTH,
)

[
    unisono_event.set_parameter("non_terminal_pair", non_terminal_pair)
    for unisono_event, non_terminal_pair in zip(
        SEQUENTIAL_UNISONO_EVENT, NON_TERMINAL_PAIR_PER_SEQUENTIAL_UNISONO_EVENT
    )
]

NON_TERMINAL_PAIR_PER_SEQUENTIAL_UNISONO_EVENT = core_utilities.compute_lazy(
    "etc/.non_terminal_pair_per_sequential_unisono_event.pickled",
    force_to_compute=dfc22.configurations.FORCE_TO_COMPUTE_NON_TERMINAL_PAIR_PER_SEQUENTIAL_UNISONO_EVENT,
)(
    lambda pitch_offset, rhythm_offset, _, __, ___: dfc22_converters.SequentialUnisonoEventToNonTerminalPairTuple(
        NON_TERMINAL_PAIR_TO_PAGE_COMBINATION_TUPLE,
        pitch_offset=pitch_offset,
        rhythm_offset=rhythm_offset,
    ).convert(
        SEQUENTIAL_UNISONO_EVENT
    )
)(
    dfc22.configurations.PITCH_OFFSET,
    dfc22.configurations.RHYTHM_OFFSET,
    SEQUENTIAL_UNISONO_EVENT,
    dfc22.configurations.MAX_PAPER_GENERATION_DEPTH,
    dfc22.configurations.MINIMAL_LANGUAGE_STRUCTURE_LENGTH,
)

[
    unisono_event.set_parameter("non_terminal_pair", non_terminal_pair)
    for unisono_event, non_terminal_pair in zip(
        SEQUENTIAL_UNISONO_EVENT, NON_TERMINAL_PAIR_PER_SEQUENTIAL_UNISONO_EVENT
    )
]


# movement_set = SEQUENTIAL_UNISONO_EVENT.get_movement_set()
# available_count, unavailable_count = 0, 0
# for movement in movement_set:
#     non_terminal_pair = movement.as_non_terminal_pair
#     print(non_terminal_pair)
#     if non_terminal_pair in NON_TERMINAL_PAIR_TO_PAGE_COMBINATION_TUPLE.keys():
#         available_count += 1
#     else:
#         unavailable_count += 1


SIMULTANEOUS_EVENT_WITH_PAGES = core_utilities.compute_lazy(
    "etc/.simultaneous_unisono_event.pickled",
    force_to_compute=dfc22.configurations.FORCE_TO_COMPUTE_SIMULTANEOUS_EVENT_WITH_PAGES,
)(
    lambda _: dfc22_converters.SequentialUnisonoEventToSimultaneousEvent(
        NON_TERMINAL_PAIR_TO_PAGE_COMBINATION_TUPLE,
        reader_count=dfc22.configurations.READER_COUNT,
    ).convert(SEQUENTIAL_UNISONO_EVENT)
)(
    dfc22.configurations.READER_COUNT
)


@core_utilities.compute_lazy(
    "etc/.simultaneous_event_with_notes.pickled",
    force_to_compute=dfc22.configurations.FORCE_TO_COMPUTE_SIMULTANEOUS_EVENT_WITH_NOTES,
)
def _make_simultaneous_events_with_notes(_):
    import progressbar

    from mutwo import core_events

    nested_language_structure_to_sequential_event = (
        dfc22_converters.NestedLanguageStructureToSequentialEvent()
    )

    simultaneous_event_with_notes = core_events.SimultaneousEvent([])

    for sequential_event in SIMULTANEOUS_EVENT_WITH_PAGES:
        new_sequential_event = core_events.SequentialEvent([])
        for event in progressbar.progressbar(sequential_event):
            if isinstance(event, dfc22_events.Page):
                new_sequential_event.append(
                    nested_language_structure_to_sequential_event(event)
                )
            else:
                new_sequential_event.append(event)

        simultaneous_event_with_notes.append(new_sequential_event)

    return simultaneous_event_with_notes


SIMULTANEOUS_EVENT_WITH_NOTES = _make_simultaneous_events_with_notes(
    dfc22.configurations.READER_COUNT
)


@core_utilities.compute_lazy(
    "etc/.simultaneous_event_with_isis_friendly--_--notes.pickled",
    force_to_compute=dfc22.configurations.FORCE_TO_COMPUTE_SIMULTANEOUS_EVENT_WITH_NOTES
    or dfc22.configurations.FORCE_TO_COMPUTE_SIMULTANEOUS_EVENT_WITH_NOTES_FOR_ISIS,
)
def _make_simultaneous_events_with_isis_friendly_notes():
    import copy

    import progressbar

    from mutwo import core_events

    nested_language_structure_to_isis_friendly_nested_language_structure = (
        dfc22_converters.NestedLanguageStructureToISiSSafeNestedLanguageStructure()
    )

    nested_language_structure_to_sequential_event = (
        dfc22_converters.NestedLanguageStructureToSequentialEvent(
            dfc22_converters.WordToSequentialEvent(
                dfc22_events.NoteLikeWithVowelAndConsonantTuple
            )
        )
    )

    simultaneous_event_with_isis_friendly_notes = core_events.SimultaneousEvent([])

    for sequential_event in copy.deepcopy(SIMULTANEOUS_EVENT_WITH_PAGES):
        new_sequential_event = core_events.SequentialEvent([])
        for event in progressbar.progressbar(sequential_event):
            if isinstance(event, dfc22_events.Page):
                event = nested_language_structure_to_isis_friendly_nested_language_structure.convert(
                    event
                )
                converted_page = nested_language_structure_to_sequential_event(event)

                def is_rest(note_like):
                    return note_like.vowel == "_"

                def process_surviving_event(event0, event1):
                    event0.duration += event1.duration
                    event0.pitch_list = [music_parameters.MidiPitch(0)]

                converted_page = converted_page.tie_by(
                    lambda event0, event1: is_rest(event0) and is_rest(event1),
                    process_surviving_event,
                    mutate=False,
                )
                new_sequential_event.append(converted_page)
            else:
                new_sequential_event.append(event)

        simultaneous_event_with_isis_friendly_notes.append(new_sequential_event)

    return simultaneous_event_with_isis_friendly_notes


SIMULTANEOUS_EVENT_WITH_ISIS_FRIENDLY_NOTES = (
    _make_simultaneous_events_with_isis_friendly_notes()
)
