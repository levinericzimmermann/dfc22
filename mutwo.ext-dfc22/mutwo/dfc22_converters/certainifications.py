"""Strategies to make uncertain objects less uncertain"""

import abc
import collections
import functools
import itertools
import operator
import typing

import numpy as np

from mutwo import core_converters
from mutwo import core_utilities
from mutwo import dfc22_parameters

__all__ = (
    "SpecifyUncertainElement",
    "SpecifyUncertainRange",
    "SymmetricalSpecifyUncertainRange",
    "SpecifyUncertainSet",
    "SpecifyUncertainDict",
    "SpecifyUncertainLetterElement",
    "SpecifyUncertainLetter",
    "SpecifyUncertainIsSideActiveSequence",
)


T = typing.TypeVar("T", bound=dfc22_parameters.UncertainElement)


class SpecifyUncertainElement(core_converters.abc.Converter):
    def __init__(self, seed: int =1000):
        self._random = np.random.default_rng(seed)

    @abc.abstractmethod
    def convert(
        self, uncertain_element_to_specifcy: T, n_specifications: int
    ) -> tuple[T, ...]:
        raise NotImplementedError


class SpecifyUncertainRange(SpecifyUncertainElement):
    @abc.abstractmethod
    def convert(
        self,
        uncertain_element_to_specifcy: dfc22_parameters.UncertainRange,
        n_specifications: int,
    ) -> [dfc22_parameters.UncertainRange, ...]:
        raise NotImplementedError


class SymmetricalSpecifyUncertainRange(SpecifyUncertainRange):
    """Split range to equal parts.

    :param factor: Defines overlap / gap between two
        consecutive parts.
        Set to 0 for no gap and no overlap.
        Set to 1 for equal overlap and part size.
        Set to 2 for double overlap and halved single part size.
        Set to -2 for double overlap and part size.
        Set to -1 for equal gap and equal part.
        Set to -2 for double size gap halved part.
    """

    def __init__(self, factor: float = 0):
        self._factor = factor
        super().__init__()

    def _get_specification_and_seperator_length(
        self,
        uncertain_range_to_specify: dfc22_parameters.UncertainRange,
        n_specifications: int,
    ) -> tuple[float, float]:
        n_seperators = n_specifications - 1
        specification_length = uncertain_range_to_specify.length() / (
            n_specifications + (n_seperators * abs(self._factor))
        )
        seperator_length = specification_length * abs(self._factor)
        return specification_length, seperator_length

    def _get_position_tuple(
        self,
        uncertain_range_to_specify: dfc22_parameters.UncertainRange,
        n_specifications: int,
        specification_length: float,
        seperator_length: float,
    ) -> tuple[float, ...]:
        length_cycle = itertools.cycle((specification_length, seperator_length))
        n_items = (n_specifications * 2) - 1
        return tuple(
            core_utilities.accumulate_from_n(
                (next(length_cycle) for _ in range(n_items)),
                uncertain_range_to_specify.start,  # type: ignore
            )
        )

    def _convert_to_parts_with_overlaps(
        self,
        uncertain_range_to_specify: dfc22_parameters.UncertainRange,
        n_specifications: int,
    ) -> tuple[dfc22_parameters.UncertainRange, ...]:
        (
            specification_length,
            seperator_length,
        ) = self._get_specification_and_seperator_length(
            uncertain_range_to_specify, n_specifications
        )
        position_tuple = self._get_position_tuple(
            uncertain_range_to_specify,
            n_specifications,
            specification_length,
            seperator_length,
        )
        n_items = len(position_tuple)
        specified_range_list = []
        for nth_item, start in enumerate(position_tuple[::2]):
            nth_item *= 2
            if nth_item + 2 != n_items:
                end = start + specification_length + seperator_length
            else:
                end = start + specification_length
            if nth_item != 0:
                start -= seperator_length

            specified_range = dfc22_parameters.UncertainRange(
                start,
                end,
                resolution_strategy=uncertain_range_to_specify.resolution_strategy,
            )
            specified_range_list.append(specified_range)
        # To ensure two ranges don't produce the same outputs
        self._random.shuffle(specified_range_list)
        return tuple(specified_range_list)

    def _convert_to_parts_with_gaps(
        self,
        uncertain_range_to_specify: dfc22_parameters.UncertainRange,
        n_specifications: int,
    ) -> tuple[dfc22_parameters.UncertainRange, ...]:
        (
            specification_length,
            seperator_length,
        ) = self._get_specification_and_seperator_length(
            uncertain_range_to_specify, n_specifications
        )
        position_tuple = self._get_position_tuple(
            uncertain_range_to_specify,
            n_specifications,
            specification_length,
            seperator_length,
        )
        specified_range_list = []
        for start, end in zip(position_tuple[::2], position_tuple[1::2]):
            specified_range = dfc22_parameters.UncertainRange(
                start,
                end,
                resolution_strategy=uncertain_range_to_specify.resolution_strategy,
            )
            specified_range_list.append(specified_range)
        return tuple(specified_range_list)

    def convert(
        self,
        uncertain_element_to_specifcy: dfc22_parameters.UncertainRange,
        n_specifications: int,
    ) -> tuple[dfc22_parameters.UncertainRange, ...]:
        assert n_specifications > 0

        if self._factor > 0:
            return self._convert_to_parts_with_overlaps(
                uncertain_element_to_specifcy, n_specifications
            )
        else:
            return self._convert_to_parts_with_gaps(
                uncertain_element_to_specifcy, n_specifications
            )


class SpecifyUncertainSet(SpecifyUncertainElement):
    """Specify uncertain set to less uncertain sets.

    :param percentage_of_elements_per_specification: How many elements
        each specification gets. If == 1 then each specification gets
        all elements which are in the original set. If == 0.5 then each
        specification gets half of all elements which are in the original.
    """

    def __init__(self, percentage_of_elements_per_specification: float = 0.25):
        super().__init__()
        self._percentage_of_elements_per_specification = (
            percentage_of_elements_per_specification
        )

    def _get_item_tuple_cycle(self, item_sequence: typing.Sequence[typing.Any]):
        n_items_in_original = len(item_sequence)
        n_items_per_specification = int(
            n_items_in_original * self._percentage_of_elements_per_specification
        )
        n_items_per_specification = (
            n_items_per_specification
            if n_items_per_specification
            else min((1, n_items_in_original))
        )
        item_tuple_cycle = itertools.cycle(
            itertools.combinations(item_sequence, n_items_per_specification)
        )
        return item_tuple_cycle

    def convert(
        self,
        uncertain_element_to_specifcy: dfc22_parameters.UncertainSet,
        n_specifications: int,
    ) -> tuple[dfc22_parameters.UncertainSet, ...]:
        assert n_specifications > 0
        item_tuple_cycle = self._get_item_tuple_cycle(
            tuple(uncertain_element_to_specifcy)
        )
        specified_set_list = []
        for _ in range(n_specifications):
            uncertain_set = dfc22_parameters.UncertainSet(
                next(item_tuple_cycle),
                resolution_strategy=uncertain_element_to_specifcy.resolution_strategy,
            )
            specified_set_list.append(uncertain_set)
        self._random.shuffle(specified_set_list)
        return tuple(specified_set_list)


class SpecifyUncertainSetAndSpecifyChildElements(SpecifyUncertainSet):
    def __init__(self, *args, specify_child_element: SpecifyUncertainElement, **kwargs):
        self._specify_child_element = specify_child_element
        super().__init__(*args, **kwargs)

    def convert(
        self,
        uncertain_element_to_specifcy: dfc22_parameters.UncertainSet,
        n_specifications: int,
    ) -> tuple[dfc22_parameters.UncertainSet, ...]:
        assert n_specifications > 0
        n_items = len(uncertain_element_to_specifcy)
        item_index_tuple_cycle = self._get_item_tuple_cycle(tuple(range(n_items)))
        item_tuple = tuple(uncertain_element_to_specifcy)
        item_index_tuple_per_specified_set_list = []
        for _ in range(n_specifications):
            item_index_tuple_per_specified_set_list.append(next(item_index_tuple_cycle))
        item_index_counter = collections.Counter(
            functools.reduce(operator.add, item_index_tuple_per_specified_set_list)
        )
        specified_child_iterator = tuple(
            iter(
                self._specify_child_element(
                    item_tuple[item_index], item_index_counter[item_index]
                )
            )
            for item_index in range(n_items)
            if item_index_counter[item_index]
        )
        specified_set_list = []
        for item_index_tuple in item_index_tuple_per_specified_set_list:
            item_list = []
            for item_index in item_index_tuple:
                item_list.append(next(specified_child_iterator[item_index]))
            uncertain_set = dfc22_parameters.UncertainSet(
                tuple(item_list),
                resolution_strategy=uncertain_element_to_specifcy.resolution_strategy,
            )
            specified_set_list.append(uncertain_set)
        return tuple(specified_set_list)


class SpecifyUncertainDict(SpecifyUncertainSet):
    def convert(
        self,
        uncertain_element_to_specifcy: dfc22_parameters.UncertainDict,
        n_specifications: int,
    ) -> tuple[dfc22_parameters.UncertainSet, ...]:
        assert n_specifications > 0
        item_tuple_cycle = self._get_item_tuple_cycle(
            tuple(uncertain_element_to_specifcy.items())
        )
        specified_dict_list = []
        for _ in range(n_specifications):
            uncertain_dict = dfc22_parameters.UncertainDict(
                {item: likelihood for item, likelihood in next(item_tuple_cycle)},
                resolution_strategy=uncertain_element_to_specifcy.resolution_strategy,
            )
            specified_dict_list.append(uncertain_dict)
        return tuple(specified_dict_list)


class SpecifyUncertainIsSideActiveSequence(SpecifyUncertainElement):
    def convert(
        self,
        uncertain_element_to_specifcy: dfc22_parameters.UncertainIsSideActiveSequence,
        n_specifications: int,
    ) -> tuple[dfc22_parameters.UncertainSet, ...]:
        assert n_specifications > 0
        specification_list = []
        for nth_side, side in enumerate(uncertain_element_to_specifcy):
            if not isinstance(side, bool):
                sides_before = uncertain_element_to_specifcy[:nth_side]
                sides_after = uncertain_element_to_specifcy[nth_side + 1 :]
                for state in side:
                    specification = dfc22_parameters.UncertainIsSideActiveSequence(
                        sides_before + [state] + sides_after
                    )
                    if not all([state is False for state in specification]):
                        specification_list.append(specification)
        if not specification_list:
            specification_list = [uncertain_element_to_specifcy]
        specification_cycle = itertools.cycle(specification_list)
        return tuple(next(specification_cycle) for _ in range(n_specifications))


class SpecifyUncertainLetterElement(SpecifyUncertainElement):
    def __init__(
        self,
        atomic_type_to_specification_dict: typing.Dict[
            typing.Type[dfc22_parameters.UncertainElement], SpecifyUncertainElement
        ] = {
            dfc22_parameters.UncertainRange: SymmetricalSpecifyUncertainRange(1),
            dfc22_parameters.UncertainSet: SpecifyUncertainSet(),
            dfc22_parameters.UncertainDict: SpecifyUncertainDict(),
            dfc22_parameters.UncertainIsSideActiveSequence: SpecifyUncertainIsSideActiveSequence(),
        },
    ):
        self._atomic_type_to_specification_dict = atomic_type_to_specification_dict

    def convert(
        self,
        uncertain_element_to_specifcy: dfc22_parameters.UncertainLetterElement,
        n_specifications: int,
    ):
        assert n_specifications > 0
        argument_to_specified_element_iterator_dict = {}
        for (
            argument_name,
            resolveable_object,
        ) in uncertain_element_to_specifcy.argument_to_resolvable_object_dict.items():
            try:
                specification = self._atomic_type_to_specification_dict[
                    type(resolveable_object)
                ]
            except KeyError:
                specified_element_tuple = tuple(
                    resolveable_object for _ in range(n_specifications)
                )
            else:
                specified_element_tuple = specification(
                    resolveable_object, n_specifications
                )
            argument_to_specified_element_iterator_dict.update(
                {argument_name: iter(specified_element_tuple)}
            )
        specified_element_list = []
        for _ in range(n_specifications):
            specified_element = type(uncertain_element_to_specifcy)(
                **{
                    argument: next(specified_element_iterator)
                    for argument, specified_element_iterator in argument_to_specified_element_iterator_dict.items()
                }
            )
            specified_element_list.append(specified_element)
        return tuple(specified_element_list)


class SpecifyUncertainLetter(SpecifyUncertainSetAndSpecifyChildElements):
    def __init__(
        self,
        factor: float = 0.65,
        specify_uncertain_letter_element: SpecifyUncertainLetterElement = SpecifyUncertainLetterElement(),
    ):
        super().__init__(factor, specify_child_element=specify_uncertain_letter_element)

    def convert(
        self,
        uncertain_element_to_specifcy: dfc22_parameters.UncertainLetter,
        n_specifications: int,
    ) -> tuple[dfc22_parameters.UncertainLetter, ...]:
        assert n_specifications > 0
        letter_element_list_per_specification = super().convert(
            uncertain_element_to_specifcy.argument_to_resolvable_object_dict[
                "letter_element_list"
            ],
            n_specifications,
        )
        original_letter_canvas = (
            uncertain_element_to_specifcy.argument_to_resolvable_object_dict[
                "letter_canvas"
            ]
        )
        specified_letter_list = []
        for letter_element_list in letter_element_list_per_specification:
            specified_letter = dfc22_parameters.UncertainLetter(
                dfc22_parameters.LetterCanvas(
                    original_letter_canvas.x, original_letter_canvas.y
                ),
                letter_element_list,
            )
            specified_letter_list.append(specified_letter)
        return tuple(specified_letter_list)
