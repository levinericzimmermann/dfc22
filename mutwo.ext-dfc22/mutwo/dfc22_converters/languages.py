import collections
import dataclasses
import itertools
import typing

import numpy as np

from mutwo import core_converters
from mutwo import core_constants
from mutwo import core_events
from mutwo import dfc22_events
from mutwo import dfc22_parameters
from mutwo import music_parameters
from mutwo import zimmermann_generators


__all__ = (
    "NonTerminalPair",
    "NonTerminalPairToWordTuple",
    "NonTerminalToNotFiniteResolutionTuple",
    "NonTerminalPairToNotFinitePairResolutionTuple",
    "NonTerminalPairToPageTuple",
    "WordToSequentialEvent",
    "SentenceToSequentialEvent",
    "prepare_word_for_isis",
)


@dataclasses.dataclass(frozen=True)
class NonTerminalPair(object):
    consonant: zimmermann_generators.JustIntonationPitchNonTerminal
    vowel: zimmermann_generators.JustIntonationPitchNonTerminal

    def __hash__(self) -> int:
        return hash(
            self.consonant.exponent_tuple + ("SEPERATOR",) + self.vowel.exponent_tuple
        )


class NonTerminalPairToWordTuple(core_converters.abc.Converter):
    def __init__(
        self,
        exponent_tuple_to_consonant_dict: dict[
            tuple[int, ...], dfc22_parameters.XSAMPAPhoneme
        ] = dfc22_events.constants.DEFAULT_EXPONENT_TUPLE_TO_CONSONANT_DICT,
        exponent_tuple_to_vowel_dict: dict[
            tuple[int, ...], dfc22_parameters.XSAMPAPhoneme
        ] = dfc22_events.constants.DEFAULT_EXPONENT_TUPLE_TO_VOWEL_DICT,
    ):
        self._exponent_tuple_to_consonant_dict = exponent_tuple_to_consonant_dict
        self._exponent_tuple_to_vowel_dict = exponent_tuple_to_vowel_dict

    def convert(
        self,
        non_terminal_pair_to_convert: NonTerminalPair,
        word_count: int,
    ) -> tuple[dfc22_events.Word, ...]:
        pass


NotFiniteResolution = tuple[zimmermann_generators.JustIntonationPitchNonTerminal, ...]
FiniteResolution = tuple[zimmermann_generators.JustIntonationPitchTerminal, ...]
NotFinitePairResolution = tuple[NonTerminalPair, ...]


class NonTerminalToNotFiniteResolutionTuple(core_converters.abc.Converter):
    limit = 100

    def __init__(
        self,
        pitch_based_context_free_grammar: zimmermann_generators.PitchBasedContextFreeGrammar,
    ):
        self._pitch_based_context_free_grammar = pitch_based_context_free_grammar

    def _get_not_finite_resolution_list(
        self,
        non_terminal_to_convert: zimmermann_generators.JustIntonationPitchNonTerminal,
        variation_count: int,
    ) -> list[NotFiniteResolution]:
        not_finite_resolution_list = []
        for limit in range(self.limit):
            resolution_tree = self._pitch_based_context_free_grammar.resolve(
                non_terminal_to_convert, limit=limit
            )
            not_finite_resolution_list = []
            for node in resolution_tree.nodes():
                finite_or_not_finite_resolution = node.data
                if all(
                    map(
                        lambda terminal_or_non_terminal: isinstance(
                            terminal_or_non_terminal,
                            zimmermann_generators.JustIntonationPitchNonTerminal,
                        ),
                        finite_or_not_finite_resolution,
                    )
                ):
                    if (
                        finite_or_not_finite_resolution
                        not in not_finite_resolution_list
                    ):
                        not_finite_resolution_list.append(
                            finite_or_not_finite_resolution
                        )
            if len(not_finite_resolution_list) >= variation_count:
                break
        return not_finite_resolution_list

    @staticmethod
    def _get_size_to_not_finite_resolution_list_dict(
        not_finite_resolution_list: list[NotFiniteResolution],
    ) -> dict[int, list[NotFiniteResolution]]:
        size_to_not_finite_resolution_list_dict = {}
        for not_finite_resolution in not_finite_resolution_list:
            not_finite_resolution_count = len(not_finite_resolution)
            if (
                not_finite_resolution_count
                not in size_to_not_finite_resolution_list_dict
            ):
                size_to_not_finite_resolution_list_dict.update(
                    {not_finite_resolution_count: []}
                )
            size_to_not_finite_resolution_list_dict[not_finite_resolution_count].append(
                not_finite_resolution
            )
        return size_to_not_finite_resolution_list_dict

    @staticmethod
    def _select_from_not_finite_resolution_list(
        not_finite_resolution_list_to_select_from: list[NotFiniteResolution],
        choosen_not_finite_resolution_list: list[NotFiniteResolution],
        select_count: int,
    ) -> list[NotFiniteResolution]:
        non_terminal_counter: dict[
            zimmermann_generators.JustIntonationPitchNonTerminal, int
        ] = collections.Counter([])
        for choosen_not_finite_resolution in choosen_not_finite_resolution_list:
            for non_terminal in choosen_not_finite_resolution:
                non_terminal_counter.update({non_terminal: 1})
        counter_index_to_not_finite_resolution_list_dict = {}
        for (
            selectable_not_finite_resolution
        ) in not_finite_resolution_list_to_select_from:
            counter_index = sum(
                [
                    non_terminal_counter[non_terminal]
                    for non_terminal in selectable_not_finite_resolution
                ]
            )
            if counter_index not in counter_index_to_not_finite_resolution_list_dict:
                counter_index_to_not_finite_resolution_list_dict.update(
                    {counter_index: []}
                )
            counter_index_to_not_finite_resolution_list_dict[counter_index].append(
                selectable_not_finite_resolution
            )
        selected_not_finite_resolution_list = []
        for counter_index in sorted(
            counter_index_to_not_finite_resolution_list_dict.keys()
        ):
            not_finite_resolution_list_with_specified_counter_index = (
                counter_index_to_not_finite_resolution_list_dict[counter_index]
            )
            for (
                not_finite_resolution
            ) in not_finite_resolution_list_with_specified_counter_index:
                if select_count > 0:
                    selected_not_finite_resolution_list.append(not_finite_resolution)
                    select_count -= 1
                else:
                    break
        return selected_not_finite_resolution_list

    @staticmethod
    def _reduce_not_finite_resolution_list(
        not_finite_resolution_list: list[NotFiniteResolution],
        variation_count: int,
    ) -> list[NotFiniteResolution]:
        size_to_not_finite_resolution_list_dict = NonTerminalToNotFiniteResolutionTuple._get_size_to_not_finite_resolution_list_dict(
            not_finite_resolution_list
        )
        filtered_not_finite_resolution_list = []
        for size in sorted(size_to_not_finite_resolution_list_dict.keys()):
            not_finite_resolution_list_part = size_to_not_finite_resolution_list_dict[
                size
            ]
            not_finite_resolution_list_part_count = len(not_finite_resolution_list_part)
            missing_not_finite_resolution_count = variation_count - len(
                filtered_not_finite_resolution_list
            )
            difference = (
                missing_not_finite_resolution_count
                - not_finite_resolution_list_part_count
            )
            if difference > 0:
                filtered_not_finite_resolution_list.extend(
                    not_finite_resolution_list_part
                )
            elif difference == 0:
                break
            # In this case we have to make a decision which resolutions
            # we don't use. We count how often the NonTerminal inside the
            # resolutions already appeared previously, the less the better
            # (we want more variation and more balance).
            else:
                filtered_not_finite_resolution_list.extend(
                    NonTerminalToNotFiniteResolutionTuple._select_from_not_finite_resolution_list(
                        not_finite_resolution_list_part,
                        filtered_not_finite_resolution_list,
                        missing_not_finite_resolution_count,
                    )
                )

        return filtered_not_finite_resolution_list

    def convert(
        self,
        non_terminal_to_convert: zimmermann_generators.JustIntonationPitchNonTerminal,
        variation_count: int = 1,
    ) -> tuple[NotFiniteResolution, ...]:
        not_finite_resolution_list = self._reduce_not_finite_resolution_list(
            self._get_not_finite_resolution_list(
                non_terminal_to_convert, variation_count
            )
        )
        return tuple(not_finite_resolution_list)


class NonTerminalPairToNotFinitePairResolutionTuple(core_converters.abc.Converter):
    def __init__(
        self,
        non_terminal_to_not_finite_resolution_tuple_for_consonants: NonTerminalToNotFiniteResolutionTuple = NonTerminalToNotFiniteResolutionTuple(
            dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS
        ),
        non_terminal_to_not_finite_resolution_tuple_for_vowels: NonTerminalToNotFiniteResolutionTuple = NonTerminalToNotFiniteResolutionTuple(
            dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS
        ),
    ):
        self._non_terminal_to_not_finite_resolution_tuple_for_consonants = (
            non_terminal_to_not_finite_resolution_tuple_for_consonants
        )
        self._non_terminal_to_not_finite_resolution_tuple_for_vowels = (
            non_terminal_to_not_finite_resolution_tuple_for_vowels
        )

    def _get_phoneme_type_to_sorted_not_finite_resolution_tuple(
        self,
        non_terminal_pair_to_convert: NonTerminalPair,
        variation_count: int,
    ):
        phoneme_type_to_sorted_not_finite_resolution_tuple = {}
        for (
            phoneme_type,
            non_terminal_to_not_finite_resolution_tuple,
            non_terminal_pair_to_convert,
        ) in (
            (
                "consonant",
                self._non_terminal_to_not_finite_resolution_tuple_for_consonants,
                non_terminal_pair_to_convert.consonant,
            ),
            (
                "vowel",
                self._non_terminal_to_not_finite_resolution_tuple_for_vowels,
                non_terminal_pair_to_convert.vowel,
            ),
        ):
            not_finite_resolution_tuple = (
                non_terminal_to_not_finite_resolution_tuple.convert(
                    non_terminal_pair_to_convert, variation_count
                )
            )
            sorted_not_finite_resolution_tuple = sorted(
                not_finite_resolution_tuple, key=len
            )
            phoneme_type_to_sorted_not_finite_resolution_tuple.update(
                {phoneme_type: sorted_not_finite_resolution_tuple}
            )
        return phoneme_type_to_sorted_not_finite_resolution_tuple

    @staticmethod
    def _balance_not_finite_resolution_pair(
        *not_finite_resolution_pair,
    ) -> tuple[NotFiniteResolution, NotFiniteResolution]:
        assert len(not_finite_resolution_pair) == 2
        difference = len(not_finite_resolution_pair[0]) - len(
            not_finite_resolution_pair[1]
        )
        non_terminal_to_add_list = [
            zimmermann_generators.JustIntonationPitchNonTerminal("1/1")
            for _ in range(abs(difference))
        ]
        if difference > 0:
            return not_finite_resolution_pair[
                0
            ], zimmermann_generators.euclidean_interlocking(
                not_finite_resolution_pair[1], non_terminal_to_add_list
            )
        elif difference < 0:
            return (
                zimmermann_generators.euclidean_interlocking(
                    not_finite_resolution_pair[0], non_terminal_to_add_list
                ),
                not_finite_resolution_pair[1],
            )
        else:
            return not_finite_resolution_pair  # type: ignore

    def convert(
        self,
        non_terminal_pair_to_convert: NonTerminalPair,
        variation_count: int = 1,
    ) -> tuple[NotFinitePairResolution, ...]:
        phoneme_type_to_sorted_not_finite_resolution_tuple = (
            self._get_phoneme_type_to_sorted_not_finite_resolution_tuple(
                non_terminal_pair_to_convert, variation_count
            )
        )

        not_finite_pair_resolution_list = []
        for consonant_not_finite_resolution, vowel_not_finite_resolution in zip(
            phoneme_type_to_sorted_not_finite_resolution_tuple["consonant"],
            phoneme_type_to_sorted_not_finite_resolution_tuple["vowel"],
        ):
            # We have to ensure that both tuples are of equal size
            (
                consonant_not_finite_resolution,
                vowel_not_finite_resolution,
            ) = self._balance_not_finite_resolution_pair(
                consonant_not_finite_resolution, vowel_not_finite_resolution
            )
            not_finite_pair_resolution = []
            for consonant_non_terminal, vowel_non_terminal in zip(
                consonant_not_finite_resolution, vowel_not_finite_resolution
            ):
                non_terminal_pair = NonTerminalPair(
                    consonant_non_terminal, vowel_non_terminal
                )
                not_finite_pair_resolution.append(non_terminal_pair)
            not_finite_pair_resolution_list.append(tuple(not_finite_pair_resolution))
        return tuple(not_finite_pair_resolution_list)


class NonTerminalPairToPageTuple(core_converters.abc.Converter):
    def __init__(
        self,
        non_terminal_pair_to_not_finite_pair_resolution_tuple_dict: dict[
            NonTerminalPair,
            tuple[NotFinitePairResolution, ...],
        ],
        non_terminal_pair_to_word_tuple_dict: dict[
            NonTerminalPair, tuple[dfc22_events.Word, ...]
        ],
    ):
        # for the roots of the pages
        self._non_terminal_pair_to_not_finite_pair_resolution_tuple_dict = (
            non_terminal_pair_to_not_finite_pair_resolution_tuple_dict
        )
        # for paragraphs, sentences, words
        self._non_terminal_pair_to_not_finite_pair_resolution_cycle_dict = {
            non_terminal_pair: itertools.cycle(not_finite_pair_resolution_tuple)
            for non_terminal_pair, not_finite_pair_resolution_tuple in self._non_terminal_pair_to_not_finite_pair_resolution_tuple_dict.items()
        }
        self._non_terminal_pair_to_word_cycle_dict = {
            non_terminal_pair: itertools.cycle(word)
            for non_terminal_pair, word in non_terminal_pair_to_word_tuple_dict.items()
        }

    def _append_word(
        self,
        container_to_append_to: dfc22_events.Sentence,
        non_terminal_pair: NonTerminalPair,
    ):
        container_to_append_to.append(
            next(self._non_terminal_pair_to_word_cycle_dict[non_terminal_pair])
        )

    def _append_nested_language_structure(
        self,
        container_to_append_to: dfc22_events.NestedLanguageStructure,
        non_terminal_pair: NonTerminalPair,
        non_terminal_pair_to_not_finite_pair_resolution: dict[
            NonTerminalPair, NotFinitePairResolution
        ],
        child_container_class: typing.Type[dfc22_events.NestedLanguageStructure],
    ):
        child_container = child_container_class()
        if non_terminal_pair in non_terminal_pair_to_not_finite_pair_resolution:
            child_not_finite_pair_resolution = (
                non_terminal_pair_to_not_finite_pair_resolution[non_terminal_pair]
            )
        else:
            child_not_finite_pair_resolution = next(
                self._non_terminal_pair_to_not_finite_pair_resolution_cycle_dict[
                    non_terminal_pair
                ]
            )
            non_terminal_pair_to_not_finite_pair_resolution.update(
                {non_terminal_pair: child_not_finite_pair_resolution}
            )
        self._convert(
            child_container,
            child_not_finite_pair_resolution,
            non_terminal_pair_to_not_finite_pair_resolution,
        )
        container_to_append_to.append(child_container)

    def _convert(
        self,
        container_to_append_to: dfc22_events.NestedLanguageStructure,
        not_finite_pair_resolution: NotFinitePairResolution,
        non_terminal_pair_to_not_finite_pair_resolution: dict[
            NonTerminalPair, NotFinitePairResolution
        ],
    ):
        child_container_class = typing.get_args(
            container_to_append_to.__orig_bases__[0]
        )[0]
        is_word = child_container_class == dfc22_events.Word
        for non_terminal_pair in not_finite_pair_resolution:
            if is_word:
                self._append_word(
                    container_to_append_to,
                    non_terminal_pair,
                )
            else:
                self._append_nested_language_structure(
                    container_to_append_to,
                    non_terminal_pair,
                    non_terminal_pair_to_not_finite_pair_resolution,
                    child_container_class,
                )

    def convert(
        self,
        non_terminal_pair_to_convert: NonTerminalPair,
    ) -> tuple[dfc22_events.Page, ...]:
        try:
            not_finite_pair_resolution_tuple = (
                self._non_terminal_pair_to_not_finite_pair_resolution_tuple_dict[
                    non_terminal_pair_to_convert
                ]
            )
        except KeyError:
            raise KeyError(
                "The provided 'NonTerminalPair' {non_terminal_pair_to_convert} "
                "couldn't be found in the given "
                "'non_terminal_pair_to_not_finite_pair_resolution'. "
                "Only the following 'NonTerminalPair' are available: "
                f"{self._non_terminal_pair_to_not_finite_pair_resolution_tuple_dict.keys()}."
            )
        page_list = []
        for root_resolution in not_finite_pair_resolution_tuple:
            non_terminal_pair_to_not_finite_pair_resolution = {
                non_terminal_pair_to_convert: root_resolution
            }
            page = dfc22_events.Page([])
            self._convert(
                page, root_resolution, non_terminal_pair_to_not_finite_pair_resolution
            )
            page_list.append(page)

        return tuple(page_list)


def find_duration(
    initial_pulse: music_parameters.JustIntonationPitch,
    uncertain_duration: dfc22_parameters.UncertainRange,
    random: np.random.Generator,
) -> core_constants.DurationType:
    pulse_list = []
    ratio = initial_pulse.ratio
    current_pulse = ratio
    while True:
        if current_pulse > uncertain_duration.end:
            break
        elif current_pulse >= uncertain_duration.start:
            pulse_list.append(current_pulse)
        current_pulse += ratio

    if not pulse_list:
        pulse_list = [ratio]

    return float(random.choice(pulse_list, 1)[0])


def make_rest(
    event_class: typing.Type,
    initial_pulse: music_parameters.JustIntonationPitch,
    uncertain_duration: dfc22_parameters.UncertainRange,
    random: np.random.Generator,
) -> typing.Union[
    dfc22_events.NoteLikeWithPhoneme,
    dfc22_events.NoteLikeWithVowelAndConsonantTuple,
]:
    keyword_argument_dict = {
        "duration": find_duration(initial_pulse, uncertain_duration, random),
    }
    if event_class == dfc22_events.NoteLikeWithPhoneme:
        keyword_argument_dict.update({"phoneme": "_", "pitch_list": []})
    elif event_class == dfc22_events.NoteLikeWithVowelAndConsonantTuple:
        keyword_argument_dict.update(
            {
                "vowel": "_",
                "consonant_tuple": tuple([]),
                "pitch_list": [music_parameters.MidiPitch(0)],
            }
        )
    return event_class(**keyword_argument_dict)


# TODO(REPLACE BY NestedLanguageStructureToISiSSafeNestedLanguageStructure)
def prepare_word_for_isis(word: dfc22_events.Word):
    """Tie events with consonants to events with vowels"""

    def process_surviving_event(phoneme_group0, phoneme_group1):
        phoneme_group0.phoneme_list.extend(phoneme_group1.phoneme_list)
        phoneme_group0.uncertain_duration = dfc22_parameters.UncertainRange(
            phoneme_group0.uncertain_duration.start
            + phoneme_group1.uncertain_duration.start,
            phoneme_group0.uncertain_duration.end
            + phoneme_group1.uncertain_duration.end,
        )

    word.tie_by(
        lambda phoneme_group0, phoneme_group1: all(
            [
                all([phoneme.is_consonant for phoneme in phoneme_group.phoneme_list])
                for phoneme_group in (phoneme_group0, phoneme_group1)
            ]
        ),
        process_surviving_event,
    )
    word.tie_by(
        lambda phoneme_group0, phoneme_group1: all(
            [phoneme.is_consonant for phoneme in phoneme_group0.phoneme_list]
        )
        and all([phoneme.is_vowel for phoneme in phoneme_group1.phoneme_list]),
        process_surviving_event,
    )


class NestedLanguageStructureToISiSSafeNestedLanguageStructure(
    core_converters.abc.Converter
):
    pass


class WordToSequentialEvent(core_converters.abc.Converter):
    def __init__(
        self,
        event_class: typing.Type = dfc22_events.NoteLikeWithPhoneme,
        seed: int = 100,
    ):
        self._event_class = event_class
        self._random = np.random.default_rng(seed)

    def _phoneme_group_to_event_specific_keyword_argument_dict(
        self, phoneme_group_to_convert: dfc22_events.PhonemeGroup
    ) -> dict[str, typing.Any]:
        keyword_argument_dict = {}
        if self._event_class == dfc22_events.NoteLikeWithPhoneme:
            keyword_argument_dict.update(
                {"phoneme": phoneme_group_to_convert.phoneme_list[0].phoneme}
            )
        elif self._event_class == dfc22_events.NoteLikeWithVowelAndConsonantTuple:
            consonant_list = []
            vowel = "_"

            for phoneme in phoneme_group_to_convert.phoneme_list:
                print(phoneme, phoneme.is_vowel)
                if phoneme.is_vowel:
                    vowel = phoneme.phoneme
                else:
                    consonant_list.append(phoneme.phoneme)
            # if vowel == "_":
            #     consonant_list = []

            keyword_argument_dict.update(
                {"vowel": vowel, "consonant_tuple": tuple(consonant_list)}
            )
        else:
            raise NotImplementedError()

        return keyword_argument_dict

    def _phoneme_group_to_duration(
        self,
        phoneme_group_to_convert: dfc22_events.PhonemeGroup,
        initial_pulse: music_parameters.JustIntonationPitch,
    ) -> core_constants.DurationType:
        return find_duration(
            initial_pulse, phoneme_group_to_convert.uncertain_duration, self._random
        )

    def _phoneme_group_to_note_like(
        self,
        phoneme_group_to_convert: dfc22_events.PhonemeGroup,
        initial_pitch: music_parameters.JustIntonationPitch,
        initial_pulse: music_parameters.JustIntonationPitch,
    ) -> tuple[
        typing.Union[
            dfc22_events.NoteLikeWithPhoneme,
            dfc22_events.NoteLikeWithVowelAndConsonantTuple,
        ],
        music_parameters.JustIntonationPitch,
        music_parameters.JustIntonationPitch,
    ]:
        keyword_argument_dict = (
            self._phoneme_group_to_event_specific_keyword_argument_dict(
                phoneme_group_to_convert
            )
        )
        new_pitch, new_pulse = (
            initial_pitch + phoneme_group_to_convert.pitch_movement,
            initial_pulse + phoneme_group_to_convert.time_movement,
        )

        keyword_argument_dict.update(
            {
                "pitch_list": [initial_pitch],
                "duration": self._phoneme_group_to_duration(
                    phoneme_group_to_convert, initial_pulse
                ),
            }
        )
        note_like = self._event_class(**keyword_argument_dict)
        return note_like, new_pitch, new_pulse

    def convert(
        self,
        word_to_convert: dfc22_events.Word,
        initial_pitch: music_parameters.JustIntonationPitch = music_parameters.JustIntonationPitch(
            "1/1"
        ),
        initial_pulse: music_parameters.JustIntonationPitch = music_parameters.JustIntonationPitch(
            "1/2"
        ),
    ) -> tuple[
        core_events.SequentialEvent[
            typing.Union[
                dfc22_events.NoteLikeWithPhoneme,
                dfc22_events.NoteLikeWithVowelAndConsonantTuple,
            ]
        ],
        music_parameters.JustIntonationPitch,
        music_parameters.JustIntonationPitch,
    ]:
        sequential_event = core_events.SequentialEvent([])
        for phoneme_group in word_to_convert:
            note_like, initial_pitch, initial_pulse = self._phoneme_group_to_note_like(
                phoneme_group, initial_pitch, initial_pulse
            )
            sequential_event.append(note_like)
        return sequential_event, initial_pitch, initial_pulse


class SentenceToSequentialEvent(core_converters.abc.Converter):
    def __init__(
        self,
        word_to_sequential_event: WordToSequentialEvent = WordToSequentialEvent(),
        seed: int = 1000,
    ):
        self._word_to_sequential_event = word_to_sequential_event
        self._uncertain_duration_rest = dfc22_parameters.UncertainRange(0.28, 0.3)
        self._random = np.random.default_rng(seed)

    def convert(
        self,
        sentence_to_convert: typing.Sequence[dfc22_events.Word],
        initial_pitch: music_parameters.JustIntonationPitch = music_parameters.JustIntonationPitch(
            "1/1"
        ),
        initial_pulse: music_parameters.JustIntonationPitch = music_parameters.JustIntonationPitch(
            "1/2"
        ),
    ) -> tuple[
        core_events.SequentialEvent[
            typing.Union[
                dfc22_events.NoteLikeWithPhoneme,
                dfc22_events.NoteLikeWithVowelAndConsonantTuple,
            ]
        ],
        music_parameters.JustIntonationPitch,
        music_parameters.JustIntonationPitch,
    ]:
        sequential_event = core_events.SequentialEvent([])
        for word in sentence_to_convert:
            (
                word_sequential_event,
                initial_pitch,
                initial_pulse,
            ) = self._word_to_sequential_event(word, initial_pitch, initial_pulse)
            sequential_event.extend(word_sequential_event)
            sequential_event.append(
                make_rest(
                    self._word_to_sequential_event._event_class,
                    initial_pulse,
                    self._uncertain_duration_rest,
                    self._random,
                )
            )
        return sequential_event, initial_pitch, initial_pulse
