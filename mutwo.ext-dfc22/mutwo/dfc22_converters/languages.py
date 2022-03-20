import collections
import functools
import itertools
import operator
import typing

import numpy as np
import progressbar

from mutwo import core_converters
from mutwo import core_constants
from mutwo import core_events
from mutwo import dfc22_converters
from mutwo import dfc22_generators
from mutwo import dfc22_events
from mutwo import dfc22_parameters
from mutwo import music_parameters
from mutwo import zimmermann_generators


__all__ = (
    "PageCatalog",
    "NonTerminalPairToWordTuple",
    "NonTerminalToNotFiniteResolutionTuple",
    "NonTerminalPairToNotFinitePairResolutionTuple",
    "NonTerminalPairToPageTuple",
    "PageCountAndWordCountToPageCatalog",
    "WordToSequentialEvent",
    "SentenceToSequentialEvent",
    "prepare_word_for_isis",
    "NestedLanguageStructureToSequentialEvent",
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
        pitch_based_context_free_grammar_for_consonants: zimmermann_generators.PitchBasedContextFreeGrammar = dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS,
        pitch_based_context_free_grammar_for_vowels: zimmermann_generators.PitchBasedContextFreeGrammar = dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS,
    ):
        self._pitch_based_context_free_grammar_for_consonants = (
            pitch_based_context_free_grammar_for_consonants
        )
        self._pitch_based_context_free_grammar_for_vowels = (
            pitch_based_context_free_grammar_for_vowels
        )
        self._exponent_tuple_to_consonant_dict = exponent_tuple_to_consonant_dict
        self._exponent_tuple_to_vowel_dict = exponent_tuple_to_vowel_dict

    def convert(
        self,
        non_terminal_pair_to_convert: dfc22_parameters.NonTerminalPair,
        word_count: int,
    ) -> tuple[dfc22_events.Word, ...]:
        # Dummy function, should later be replaced by something else
        word_tuple = dfc22_generators.make_word_tuple(
            non_terminal_pair_to_convert.consonant,
            3,
            non_terminal_pair_to_convert.vowel,
            3,
            self._pitch_based_context_free_grammar_for_consonants,
            self._pitch_based_context_free_grammar_for_vowels,
        )[:word_count]
        assert len(word_tuple) == word_count
        for word in word_tuple:
            assert word.non_terminal_pair == non_terminal_pair_to_convert
        return word_tuple


NotFiniteResolution = tuple[zimmermann_generators.JustIntonationPitchNonTerminal, ...]
FiniteResolution = tuple[zimmermann_generators.JustIntonationPitchTerminal, ...]
NotFinitePairResolution = tuple[dfc22_parameters.NonTerminalPair, ...]
PageCatalog = dict[dfc22_parameters.NonTerminalPair, tuple[dfc22_events.Page, ...]]


class NonTerminalToNotFiniteResolutionTuple(core_converters.abc.Converter):
    def __init__(
        self,
        pitch_based_context_free_grammar: zimmermann_generators.PitchBasedContextFreeGrammar,
        minimal_resolution_length: typing.Optional[int] = None,
        # The max search depth
        limit: typing.Optional[int] = None,
    ):
        if limit is None:
            limit = dfc22_converters.configurations.DEFAULT_LIMIT
        if minimal_resolution_length is None:
            minimal_resolution_length = (
                dfc22_converters.configurations.DEFAULT_MINIMAL_RESOLUTION_LENGHT
            )
        self.limit = limit
        self._pitch_based_context_free_grammar = pitch_based_context_free_grammar
        self._minimal_resolution_length = minimal_resolution_length

    def _get_not_finite_resolution_list(
        self,
        non_terminal_to_convert: zimmermann_generators.JustIntonationPitchNonTerminal,
        variation_count: int,
    ) -> list[NotFiniteResolution]:
        not_finite_resolution_list = []
        for limit in progressbar.progressbar(
            range(self.limit), prefix="Iterate limits || "
        ):
            resolution_tree = self._pitch_based_context_free_grammar.resolve(
                non_terminal_to_convert, limit=limit
            )
            not_finite_resolution_list = []
            for node in resolution_tree.nodes.values():
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
        if variation_count:
            try:
                assert not_finite_resolution_list
            except AssertionError:
                rule_string = ""
                for (
                    context_free_grammar_rule
                ) in (
                    self._pitch_based_context_free_grammar.context_free_grammar_rule_tuple
                ):
                    if context_free_grammar_rule.left_side == non_terminal_to_convert:
                        rule_string += f"{context_free_grammar_rule}\n"
                raise Exception(
                    "There is no not finite resolution for the non terminal"
                    f" '{non_terminal_to_convert}' in the grammar "
                    f"{self._pitch_based_context_free_grammar}."
                    "The related rules of the grammar are:\n\n"
                    f"{rule_string}"
                    "\nThe non terminals are:\n"
                    f"{self._pitch_based_context_free_grammar.non_terminal_tuple}"
                )
        counter = 0
        while len(not_finite_resolution_list) < variation_count:
            not_finite_resolution_list.append(not_finite_resolution_list[counter])
            counter += 1
        assert len(not_finite_resolution_list) >= variation_count
        for not_finite_resolution in not_finite_resolution_list:
            assert (
                functools.reduce(
                    operator.add,
                    (zimmermann_generators.JustIntonationPitchNonTerminal(),)
                    + not_finite_resolution,
                )
                == non_terminal_to_convert
            )
        return not_finite_resolution_list

    def _get_size_to_not_finite_resolution_list_dict(
        self,
        not_finite_resolution_list: list[NotFiniteResolution],
        variation_count: int,
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

        dropped_finite_resolution_list = []

        if any(
            [
                size > self._minimal_resolution_length
                for size in size_to_not_finite_resolution_list_dict
            ]
        ):
            size_to_not_finite_resolution_list_dict = {
                size: not_finite_resolution_list
                for size, not_finite_resolution_list in size_to_not_finite_resolution_list_dict.items()
                if size >= self._minimal_resolution_length
            }

        else:
            for (
                not_finite_resolution_list
            ) in size_to_not_finite_resolution_list_dict.values():
                dropped_finite_resolution_list.append(not_finite_resolution)

        dropped_finite_resolution_list.sort(
            key=lambda finite_resolution: len(finite_resolution), reverse=True
        )
        dropped_finite_resolution_iterator = iter(dropped_finite_resolution_list)

        while (
            sum(
                [
                    len(finite_resolution_list)
                    for finite_resolution_list in size_to_not_finite_resolution_list_dict.values()
                ]
            )
            < variation_count
        ):
            finite_resolution = next(dropped_finite_resolution_iterator)
            size = len(finite_resolution)
            if size not in size_to_not_finite_resolution_list_dict:
                size_to_not_finite_resolution_list_dict.update({size: []})
            size_to_not_finite_resolution_list_dict[size].append(finite_resolution)

        assert (
            sum(
                [
                    len(finite_resolution_list)
                    for finite_resolution_list in size_to_not_finite_resolution_list_dict.values()
                ]
            )
            >= variation_count
        )
        return size_to_not_finite_resolution_list_dict

    @staticmethod
    def _select_from_not_finite_resolution_list(
        not_finite_resolution_list_to_select_from: list[NotFiniteResolution],
        choosen_not_finite_resolution_list: list[NotFiniteResolution],
        select_count: int,
    ) -> list[NotFiniteResolution]:
        non_terminal_counter: dict[tuple[int, ...], int] = collections.Counter([])
        for choosen_not_finite_resolution in choosen_not_finite_resolution_list:
            for non_terminal in choosen_not_finite_resolution:
                non_terminal_counter.update({non_terminal.exponent_tuple: 1})
        counter_index_to_not_finite_resolution_list_dict = {}
        for (
            selectable_not_finite_resolution
        ) in not_finite_resolution_list_to_select_from:
            counter_index = sum(
                [
                    non_terminal_counter[non_terminal.exponent_tuple]
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
        select_count_down = int(select_count)
        for counter_index in sorted(
            counter_index_to_not_finite_resolution_list_dict.keys(),
            # Prefer longer language structures
            reverse=True,
        ):
            not_finite_resolution_list_with_specified_counter_index = (
                counter_index_to_not_finite_resolution_list_dict[counter_index]
            )
            for (
                not_finite_resolution
            ) in not_finite_resolution_list_with_specified_counter_index:
                if select_count_down > 0:
                    selected_not_finite_resolution_list.append(not_finite_resolution)
                    select_count_down -= 1
                else:
                    break
        assert len(selected_not_finite_resolution_list) == select_count
        return selected_not_finite_resolution_list

    def _reduce_not_finite_resolution_list(
        self,
        not_finite_resolution_list: list[NotFiniteResolution],
        variation_count: int,
    ) -> list[NotFiniteResolution]:
        size_to_not_finite_resolution_list_dict = (
            self._get_size_to_not_finite_resolution_list_dict(
                not_finite_resolution_list, variation_count
            )
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
            if difference >= 0:
                filtered_not_finite_resolution_list.extend(
                    not_finite_resolution_list_part
                )
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

        assert len(filtered_not_finite_resolution_list) == variation_count
        return filtered_not_finite_resolution_list

    def convert(
        self,
        non_terminal_to_convert: zimmermann_generators.JustIntonationPitchNonTerminal,
        variation_count: int = 1,
        limit: typing.Optional[int] = None,
    ) -> tuple[NotFiniteResolution, ...]:
        if limit:
            main_limit = int(self.limit)
            self.limit = limit
        not_finite_resolution_list = self._reduce_not_finite_resolution_list(
            self._get_not_finite_resolution_list(
                non_terminal_to_convert, variation_count
            ),
            variation_count,
        )
        assert len(not_finite_resolution_list) == variation_count
        if limit:
            self.limit = main_limit
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
        self.limit = None
        self._non_terminal_to_not_finite_resolution_tuple_for_consonants = (
            non_terminal_to_not_finite_resolution_tuple_for_consonants
        )
        self._non_terminal_to_not_finite_resolution_tuple_for_vowels = (
            non_terminal_to_not_finite_resolution_tuple_for_vowels
        )

    def _get_phoneme_type_to_sorted_not_finite_resolution_tuple(
        self,
        non_terminal_pair_to_convert: dfc22_parameters.NonTerminalPair,
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
                    non_terminal_pair_to_convert, variation_count, limit=self.limit
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
        non_terminal_pair_to_convert: dfc22_parameters.NonTerminalPair,
        variation_count: int = 1,
        limit: typing.Optional[int] = None,
    ) -> tuple[NotFinitePairResolution, ...]:
        if limit:
            main_limit = int(limit)
            self.limit = limit
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
                non_terminal_pair = dfc22_parameters.NonTerminalPair(
                    consonant_non_terminal, vowel_non_terminal
                )
                not_finite_pair_resolution.append(non_terminal_pair)
            assert (
                functools.reduce(
                    operator.add,
                    [dfc22_parameters.NonTerminalPair()] + not_finite_pair_resolution,
                )
                == non_terminal_pair_to_convert
            )
            not_finite_pair_resolution_list.append(tuple(not_finite_pair_resolution))
        if limit:
            self.limit = main_limit
        return tuple(not_finite_pair_resolution_list)


class NonTerminalPairToPageTuple(core_converters.abc.Converter):
    def __init__(
        self,
        non_terminal_pair_to_not_finite_pair_resolution_tuple_dict: dict[
            dfc22_parameters.NonTerminalPair,
            tuple[NotFinitePairResolution, ...],
        ],
        non_terminal_pair_to_word_tuple_dict: dict[
            dfc22_parameters.NonTerminalPair, tuple[dfc22_events.Word, ...]
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
            non_terminal_pair: itertools.cycle(word_tuple)
            for non_terminal_pair, word_tuple in non_terminal_pair_to_word_tuple_dict.items()
        }

    def _append_word(
        self,
        container_to_append_to: dfc22_events.Sentence,
        non_terminal_pair: dfc22_parameters.NonTerminalPair,
    ):
        word = next(self._non_terminal_pair_to_word_cycle_dict[non_terminal_pair])
        assert word.non_terminal_pair == non_terminal_pair
        container_to_append_to.append(word)

    def _append_nested_language_structure(
        self,
        container_to_append_to: dfc22_events.NestedLanguageStructure,
        non_terminal_pair: dfc22_parameters.NonTerminalPair,
        non_terminal_pair_to_not_finite_pair_resolution: dict[
            dfc22_parameters.NonTerminalPair, NotFinitePairResolution
        ],
        child_container_class: typing.Type[dfc22_events.NestedLanguageStructure],
    ):
        child_container = child_container_class([])
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
        assert child_container.non_terminal_pair == non_terminal_pair
        container_to_append_to.append(child_container)

    def _convert(
        self,
        container_to_append_to: dfc22_events.NestedLanguageStructure,
        not_finite_pair_resolution: NotFinitePairResolution,
        non_terminal_pair_to_not_finite_pair_resolution: dict[
            dfc22_parameters.NonTerminalPair, NotFinitePairResolution
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
            assert container_to_append_to[-1].non_terminal_pair == non_terminal_pair

    def convert(
        self,
        non_terminal_pair_to_convert: dfc22_parameters.NonTerminalPair,
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
            resolved = functools.reduce(
                operator.add,
                (dfc22_parameters.NonTerminalPair(),) + root_resolution,
            )
            try:
                assert resolved == non_terminal_pair_to_convert
            except AssertionError:
                raise Exception(
                    (
                        f"Wrong resolution! Expected {root_resolution}.",
                        f"Got {resolved}...",
                    )
                )
            non_terminal_pair_to_not_finite_pair_resolution = {
                non_terminal_pair_to_convert: root_resolution
            }
            page = dfc22_events.Page([])
            self._convert(
                page, root_resolution, non_terminal_pair_to_not_finite_pair_resolution
            )
            assert page.non_terminal_pair == non_terminal_pair_to_convert
            page_list.append(page)

        return tuple(page_list)


class PageCountAndWordCountToPageCatalog(core_converters.abc.Converter):
    def __init__(
        self,
        exponent_tuple_to_consonant_dict: dict[
            tuple[int, ...], dfc22_parameters.XSAMPAPhoneme
        ] = dfc22_events.constants.DEFAULT_EXPONENT_TUPLE_TO_CONSONANT_DICT,
        exponent_tuple_to_vowel_dict: dict[
            tuple[int, ...], dfc22_parameters.XSAMPAPhoneme
        ] = dfc22_events.constants.DEFAULT_EXPONENT_TUPLE_TO_VOWEL_DICT,
        pitch_based_context_free_grammar_for_consonants: zimmermann_generators.PitchBasedContextFreeGrammar = dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_CONSONANTS,
        pitch_based_context_free_grammar_for_vowels: zimmermann_generators.PitchBasedContextFreeGrammar = dfc22_parameters.constants.DEFAULT_PITCH_BASED_CONTEXT_FREE_GRAMMAR_FOR_VOWELS,
        side_limit: int = 5,
    ):
        # TODO(better decide which non terminals should belong together)
        self.side_limit = side_limit
        non_terminal_pair_list = []
        for consonant, vowel in zip(
            pitch_based_context_free_grammar_for_consonants.non_terminal_tuple,
            pitch_based_context_free_grammar_for_vowels.non_terminal_tuple,
        ):
            non_terminal_pair = dfc22_parameters.NonTerminalPair(consonant, vowel)
            non_terminal_pair_list.append(non_terminal_pair)

        all_non_terminal_pair_list = []
        for consonant, vowel in itertools.product(
            pitch_based_context_free_grammar_for_consonants.non_terminal_tuple,
            pitch_based_context_free_grammar_for_vowels.non_terminal_tuple,
        ):
            non_terminal_pair = dfc22_parameters.NonTerminalPair(consonant, vowel)
            all_non_terminal_pair_list.append(non_terminal_pair)

        self._non_terminal_pair_tuple = tuple(non_terminal_pair_list)
        self._all_non_terminal_pair_tuple = tuple(all_non_terminal_pair_list)
        self._non_terminal_pair_to_not_finite_pair_resolution_tuple = (
            NonTerminalPairToNotFinitePairResolutionTuple(
                NonTerminalToNotFiniteResolutionTuple(
                    pitch_based_context_free_grammar_for_consonants
                ),
                NonTerminalToNotFiniteResolutionTuple(
                    pitch_based_context_free_grammar_for_vowels
                ),
            )
        )
        self._non_terminal_pair_to_word_tuple = NonTerminalPairToWordTuple(
            exponent_tuple_to_consonant_dict,
            exponent_tuple_to_vowel_dict,
            pitch_based_context_free_grammar_for_consonants,
            pitch_based_context_free_grammar_for_vowels,
        )

        self._pitch_based_context_free_grammar_for_consonants = (
            pitch_based_context_free_grammar_for_consonants
        )
        self._pitch_based_context_free_grammar_for_vowels = (
            pitch_based_context_free_grammar_for_vowels
        )
        self._exponent_tuple_to_consonant_dict = exponent_tuple_to_consonant_dict
        self._exponent_tuple_to_vowel_dict = exponent_tuple_to_vowel_dict

    def _get_non_terminal_pair_to_page_tuple(
        self, page_count: int, word_count: int
    ) -> NonTerminalPairToPageTuple:
        non_terminal_pair_to_not_finite_pair_resolution_tuple_dict = {}
        for non_terminal_pair in progressbar.progressbar(
            self._non_terminal_pair_tuple,
            prefix=(
                "dfc22_converters.languages: Find not_finite_pair_resolution_tuple."
                f" Limit: {dfc22_converters.configurations.DEFAULT_LIMIT}, "
                "Minimal Length: "
                f"{dfc22_converters.configurations.DEFAULT_MINIMAL_RESOLUTION_LENGHT}"
            ),
        ):
            not_finite_pair_resolution_tuple = (
                self._non_terminal_pair_to_not_finite_pair_resolution_tuple.convert(
                    non_terminal_pair, page_count
                )
            )
            non_terminal_pair_to_not_finite_pair_resolution_tuple_dict.update(
                {non_terminal_pair: not_finite_pair_resolution_tuple}
            )
            assert len(not_finite_pair_resolution_tuple) == page_count
        non_terminal_pair_to_word_tuple_dict = {}
        for non_terminal_pair in self._all_non_terminal_pair_tuple:
            if (
                non_terminal_pair
                not in non_terminal_pair_to_not_finite_pair_resolution_tuple_dict
            ):
                not_finite_pair_resolution_tuple = (
                    self._non_terminal_pair_to_not_finite_pair_resolution_tuple.convert(
                        non_terminal_pair, page_count, limit=self.side_limit
                    )
                )
                non_terminal_pair_to_not_finite_pair_resolution_tuple_dict.update(
                    {non_terminal_pair: not_finite_pair_resolution_tuple}
                )
            word_tuple = self._non_terminal_pair_to_word_tuple.convert(
                non_terminal_pair, word_count
            )
            non_terminal_pair_to_word_tuple_dict.update({non_terminal_pair: word_tuple})
        return NonTerminalPairToPageTuple(
            non_terminal_pair_to_not_finite_pair_resolution_tuple_dict,
            non_terminal_pair_to_word_tuple_dict,
        )

    def convert(self, page_count: int, word_count: int) -> PageCatalog:
        non_terminal_pair_to_page_tuple = self._get_non_terminal_pair_to_page_tuple(
            page_count, word_count
        )
        non_terminal_pair_to_page_tuple_dict: PageCatalog = {}
        for non_terminal_pair in progressbar.progressbar(
            self._non_terminal_pair_tuple,
            prefix="dfc22_converters.languages: Convert non terminal pair",
        ):
            non_terminal_pair_to_page_tuple_dict.update(
                {
                    non_terminal_pair: non_terminal_pair_to_page_tuple.convert(
                        non_terminal_pair
                    )
                }
            )
        return non_terminal_pair_to_page_tuple_dict


def find_duration(
    initial_pulse: music_parameters.JustIntonationPitch,
    uncertain_duration: dfc22_parameters.UncertainRange,
    random: np.random.Generator,
) -> core_constants.DurationType:
    pulse_list = []
    ratio = float(initial_pulse.ratio)
    current_pulse = float(ratio)
    while True:
        if current_pulse > uncertain_duration.end:
            break
        elif current_pulse >= uncertain_duration.start:
            pulse_list.append(current_pulse)
        current_pulse += ratio

    if not pulse_list:
        pulse_list = [ratio]

    # return float(random.choice(pulse_list, 1)[0])
    return float(max(pulse_list))


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


class NestedLanguageStructureToSequentialEvent(core_converters.abc.Converter):
    def __init__(
        self, word_to_sequential_event: WordToSequentialEvent = WordToSequentialEvent()
    ):
        self._word_to_sequential_event = word_to_sequential_event

    def _append_word_to_sequential_event(
        self,
        sequential_event_to_append_to: core_events.SequentialEvent,
        word: dfc22_events.Word,
        initial_pitch: typing.Optional[music_parameters.JustIntonationPitch] = None,
        initial_pulse: typing.Optional[music_parameters.JustIntonationPitch] = None,
    ):
        word, *_ = self._word_to_sequential_event.convert(
            word, initial_pitch, initial_pulse
        )
        sequential_event_to_append_to.extend(word)

    def _convert(
        self,
        sequential_event_to_append_to: core_events.SequentialEvent,
        nested_language_structure: dfc22_events.NestedLanguageStructure,
        initial_pitch: typing.Optional[music_parameters.JustIntonationPitch] = None,
        initial_pulse: typing.Optional[music_parameters.JustIntonationPitch] = None,
    ):
        if initial_pitch is None or initial_pulse is None:
            initial_non_terminal_pair = (
                nested_language_structure.initial_non_terminal_pair
            )
        if initial_pitch is None:
            initial_pitch = initial_non_terminal_pair.vowel
        if initial_pulse is None:
            initial_pulse = initial_non_terminal_pair.consonant

        if isinstance(nested_language_structure, dfc22_events.Word):
            self._append_word_to_sequential_event(
                sequential_event_to_append_to,
                nested_language_structure,
                initial_pitch,
                initial_pulse,
            )

        elif isinstance(
            nested_language_structure, dfc22_events.NestedLanguageStructure
        ):
            for language_structure in nested_language_structure:
                self._convert(
                    sequential_event_to_append_to,
                    language_structure,
                    initial_pitch,
                    initial_pulse,
                )
                initial_pitch += language_structure.pitch_movement
                initial_pulse += language_structure.time_movement

        else:
            raise NotImplementedError(
                (
                    f"Found unexpected object '{nested_language_structure}'"
                    f"of type '{type(nested_language_structure)}'!"
                )
            )

    def convert(
        self,
        nested_language_structure: dfc22_events.NestedLanguageStructure,
        initial_pitch: typing.Optional[music_parameters.JustIntonationPitch] = None,
        initial_pulse: typing.Optional[music_parameters.JustIntonationPitch] = None,
    ) -> core_events.SequentialEvent:

        sequential_event = core_events.SequentialEvent([])
        self._convert(
            sequential_event, nested_language_structure, initial_pitch, initial_pulse
        )
        return sequential_event
