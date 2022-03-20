import copy
import functools
import operator
import itertools
import typing

import progressbar

from mutwo import core_converters
from mutwo import core_events
from mutwo import core_utilities
from mutwo import dfc22_converters
from mutwo import dfc22_events
from mutwo import dfc22_parameters
from mutwo import zimmermann_generators


__all__ = (
    "ReaderCountToSequentialUnisonoEvent",
    "PageCatalogToPageCombinationCatalog",
    "SequentialUnisonoEventToPageTuple",
    "SequentialUnisonoEventToNonTerminalPairTuple",
    "SequentialUnisonoEventToSimultaneousEvent",
)

PageCombinationCatalog = dict[
    dfc22_parameters.NonTerminalPair, tuple[tuple[dfc22_events.Page, ...], ...]
]


class ReaderCountToSequentialUnisonoEvent(core_converters.abc.Converter):
    def __init__(
        self,
        min_reader_combination_count: int = 1,
        max_reader_combination_count: int = 3,
    ):
        self._min_reader_combination_count = min_reader_combination_count
        self._max_reader_combination_count = max_reader_combination_count

    def convert(self, reader_count: int) -> dfc22_events.SequentialUnisonoEvent:
        reader_index_range = range(reader_count)
        reader_combination_tuple_list = []
        for reader_to_combine_count in range(
            self._min_reader_combination_count,
            min((self._max_reader_combination_count + 1, reader_count + 1)),
        ):
            reader_index_combination_tuple = tuple(
                itertools.combinations(reader_index_range, reader_to_combine_count)
            )
            if reader_to_combine_count % 2 == 0:
                reader_combination_tuple_list.append(reader_index_combination_tuple)
            else:
                reader_index_combination_tuple = tuple(
                    reversed(reader_index_combination_tuple)
                )
                reader_combination_tuple_list.insert(0, reader_index_combination_tuple)
        reader_combination_tuple = zimmermann_generators.euclidean_interlocking(
            *reader_combination_tuple_list
        )
        # reader_combination_tuple_cycle = core_utilities.cyclic_permutations(
        #     reader_combination_tuple
        # )
        # while len(reader_combination_tuple[0]) != reader_count:
        #     reader_combination_tuple = next(reader_combination_tuple_cycle)
        sequential_unisono_event = dfc22_events.SequentialUnisonoEvent(
            [
                dfc22_events.UnisonoEvent(reader_tuple)
                for reader_tuple in reader_combination_tuple
            ]
        )
        return sequential_unisono_event


class PageCatalogToPageCombinationCatalog(core_converters.abc.Converter):
    def __init__(
        self,
        maximum_page_combination_count: typing.Optional[int] = None,
        minimal_page_combination_count: typing.Optional[int] = None,
    ):
        if not maximum_page_combination_count:
            maximum_page_combination_count = (
                dfc22_converters.configurations.DEFAULT_MAXIMUM_PAGE_COMBINATION_COUNT
            )
        if not minimal_page_combination_count:
            minimal_page_combination_count = (
                dfc22_converters.configurations.DEFAULT_MINIMAL_PAGE_COMBINATION_COUNT
            )
        self._maximum_page_combination_count = maximum_page_combination_count
        self._minimal_page_combination_count = minimal_page_combination_count

    def _make_non_terminal_pair_to_page_combination_list(
        self,
        page_catalog_to_convert: dfc22_converters.PageCatalog,
    ) -> dict[dfc22_parameters.NonTerminalPair, list[tuple[dfc22_events.Page, ...]]]:
        non_terminal_pair_tuple = tuple(page_catalog_to_convert.keys())
        non_terminal_pair_to_page_combination_list = {}
        for combination_count in range(1, self._maximum_page_combination_count + 1):
            for non_terminal_pair_combination in progressbar.progressbar(
                itertools.combinations_with_replacement(
                    non_terminal_pair_tuple, combination_count
                ),
                prefix="Find non_terminal_pair_to_page_combination_list",
            ):
                reduced_non_terminal_pair = functools.reduce(
                    operator.add, non_terminal_pair_combination
                )
                if (
                    reduced_non_terminal_pair
                    not in non_terminal_pair_to_page_combination_list
                ):
                    non_terminal_pair_to_page_combination_list.update(
                        {reduced_non_terminal_pair: []}
                    )
                for page_tuple in itertools.product(
                    *[
                        page_catalog_to_convert[non_terminal_pair]
                        for non_terminal_pair in non_terminal_pair_combination
                    ]
                ):
                    for page_tuple_variant in itertools.permutations(page_tuple):
                        non_terminal_pair_to_page_combination_list[
                            reduced_non_terminal_pair
                        ].append(page_tuple_variant)
        return non_terminal_pair_to_page_combination_list

    def convert(
        self, page_catalog_to_convert: dfc22_converters.PageCatalog
    ) -> PageCombinationCatalog:
        non_terminal_pair_to_page_combination_list = (
            self._make_non_terminal_pair_to_page_combination_list(
                page_catalog_to_convert
            )
        )
        non_terminal_pair_to_page_combination_tuple = {
            non_terminal_pair: tuple(set(page_tuple_list))
            for non_terminal_pair, page_tuple_list in non_terminal_pair_to_page_combination_list.items()
        }
        # Only use those which are more flexible and which offer various
        # solutions (so that we can better pick more harmonic results)
        filtered_non_terminal_pair_to_page_combination_tuple = {
            non_terminal_pair: page_tuple_list
            for non_terminal_pair, page_tuple_list in non_terminal_pair_to_page_combination_tuple.items()
            if len(page_tuple_list) > self._minimal_page_combination_count
        }
        return filtered_non_terminal_pair_to_page_combination_tuple


class SequentialUnisonoEventConverter(core_converters.abc.Converter):
    def __init__(self, page_combination_catalog: PageCombinationCatalog):
        self._page_combination_catalog = page_combination_catalog


class SequentialUnisonoEventToPageTuple(core_converters.abc.Converter):
    def __init__(self, page_catalog: dfc22_converters.PageCatalog):
        self._nested_page_tuple = tuple(page_catalog.values())

    def convert(
        self, sequential_unisono_event_to_convert: dfc22_events.SequentialUnisonoEvent
    ) -> tuple[dfc22_events.Page, ...]:
        nested_page_list = []
        max_page_count = max(
            [len(page_tuple) for page_tuple in self._nested_page_tuple]
        )
        cyclic_permutation_index_cycle = itertools.cycle(
            zimmermann_generators.euclidean_interlocking(
                tuple(range(max_page_count)),
                tuple(reversed(tuple(range(max_page_count)))),
                tuple(range(1, max_page_count)),
            )
        )
        for index, page_tuple in enumerate(self._nested_page_tuple):
            if index % 2 == 0:
                page_tuple = tuple(reversed(page_tuple))
            page_tuple_iterator = core_utilities.cyclic_permutations(page_tuple)
            for _ in range(next(cyclic_permutation_index_cycle)):
                page_tuple = next(page_tuple_iterator)
            nested_page_list.append(page_tuple)

        page_cycle_list = [
            itertools.cycle(page_tuple) for page_tuple in nested_page_list
        ]
        page_index_tuple_cycle = itertools.cycle(
            itertools.permutations(range(len(self._nested_page_tuple)))
        )
        page_list = []
        page_index_iterator = iter([])
        for _ in sequential_unisono_event_to_convert:
            try:
                page_index = next(page_index_iterator)
            except StopIteration:
                page_index_iterator = iter(next(page_index_tuple_cycle))
                page_index = next(page_index_iterator)
            page_list.append(next(page_cycle_list[page_index]))
        return tuple(page_list)


class SequentialUnisonoEventToNonTerminalPairTuple(SequentialUnisonoEventConverter):
    def __init__(
        self,
        *args,
        pitch_offset: zimmermann_generators.JustIntonationPitchNonTerminal = zimmermann_generators.JustIntonationPitchNonTerminal(),
        rhythm_offset: zimmermann_generators.JustIntonationPitchNonTerminal = zimmermann_generators.JustIntonationPitchNonTerminal(),
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._non_terminal_pair_offset = dfc22_parameters.NonTerminalPair(
            consonant=rhythm_offset, vowel=pitch_offset
        )

    def convert(
        self, sequential_unisono_event_to_convert: dfc22_events.SequentialUnisonoEvent
    ) -> tuple[dfc22_parameters.NonTerminalPair, ...]:
        non_terminal_pair_list = []
        for unisono_event in sequential_unisono_event_to_convert:
            non_terminal_pair_list.append(
                unisono_event.page.non_terminal_pair + self._non_terminal_pair_offset
            )

        non_terminal_pair_list = (
            non_terminal_pair_list[-1:] + non_terminal_pair_list[:-1]
        )

        # return tuple(
        #     dfc22_parameters.NonTerminalPair(
        #         zimmermann_generators.JustIntonationPitchNonTerminal(),
        #         zimmermann_generators.JustIntonationPitchNonTerminal(),
        #     )
        #     for _ in sequential_unisono_event_to_convert
        # )

        return tuple(non_terminal_pair_list)


class SequentialUnisonoEventToSimultaneousEvent(SequentialUnisonoEventConverter):
    def __init__(self, *args, reader_count: int, **kwargs):
        super().__init__(*args, **kwargs)
        self._reader_count = reader_count

    # jede valide verbindung muss eine konkrete interpolation aussuchen
    # (also eine range von 0 bis len(solution_tuple))

    # das loesen der abstrakten daten funktioniert so...

    # ...danach koennen wir die einzelnen interpolationen sowie die unisono teile konkret
    #    in die zeit setzen. dafuer werden zuerst leere sequential event, eins fuer jede
    #    stimme, generiert.
    #    dann werden zuerst die unisono teile gesetzt: immer in die mitte, links eine
    #    haelfte der pause, rechts eine haelfte der pause.
    #    danach werden die interpolation verteilt. so dass zwischen den seiten (auch ganz vorne und
    #    ganz hinten) gleich lange pausen entstehen.
    #
    #    dann werden die pausen noch korrekter gesetzt, dass sie auch eine bestimmte tonhoehe
    #    und einen bestimmten puls haben (naemlich die, die zuletzt gegolten haben). dafuer wird einfach
    #    den gerundet naehsten puls genommen (also wie viele von den gegenwaertig geltendend pulsen muss
    #    ich multiplizieren, um am ende moeglichst auf die dauer der pause zu kommen). vielleicht kann
    #    es dabei zu kleinen verschiebungen kommen? aber das werde ich noch raus finden

    # ...danach kann bestimmt werden wie "harmonisch" die gewaehlte loesung ist.

    class DataToSimultaneousEvent(core_converters.abc.Converter):
        PAGE_BUFFER_DURATION = 2.5

        def __init__(self, reader_count: int):
            self._reader_count = reader_count

        def _set_unisono_events_duration(
            self,
            page_combination_tuple: tuple[tuple[dfc22_events.Page, ...], ...],
            sequential_unisono_event_to_convert: dfc22_events.SequentialUnisonoEvent,
            movement_tuple: tuple[dfc22_events.SequentialUnisonoEvent.Movement, ...],
        ):
            """Adjust the duration of the unisono events according to
            the interpolations"""

            unisono_event_count = len(sequential_unisono_event_to_convert)
            for page_combination, movement in zip(
                page_combination_tuple, movement_tuple
            ):
                minimal_duration = sum(page.duration for page in page_combination) + (
                    len(page_combination) * self.PAGE_BUFFER_DURATION
                )
                left_index, right_index = (
                    movement.unisono_event_left_index,
                    movement.unisono_event_right_index,
                )
                is_short_interpolation = True
                if right_index - left_index > 1:
                    is_short_interpolation = False
                    left_index += 1
                local_unisono_event_count = (
                    right_index - left_index
                ) % unisono_event_count
                minimal_duration_for_one_unisono_event = (
                    minimal_duration / local_unisono_event_count
                )
                if left_index < right_index:
                    unisono_event_index_list = list(range(left_index, right_index))
                else:
                    unisono_event_index_list = list(
                        range(left_index, unisono_event_count)
                    )
                    unisono_event_index_list.extend(list(range(0, right_index)))
                for unisono_event_index in unisono_event_index_list:
                    unisono_event = sequential_unisono_event_to_convert[
                        unisono_event_index
                    ]

                    if is_short_interpolation:
                        local_minimal_duration_for_one_unisono_event = (
                            unisono_event.page.duration
                            + minimal_duration_for_one_unisono_event
                        )
                    else:
                        local_minimal_duration_for_one_unisono_event = (
                            minimal_duration_for_one_unisono_event
                        )
                    if (
                        unisono_event.duration
                        < local_minimal_duration_for_one_unisono_event
                    ):
                        unisono_event.duration = (
                            local_minimal_duration_for_one_unisono_event
                        )

        def _insert_unisono_events(
            self,
            sequential_unisono_event_to_convert: dfc22_events.SequentialUnisonoEvent,
            simultaneous_event: core_events.SimultaneousEvent,
        ) -> tuple[tuple[float, ...], tuple[float, ...]]:
            unisono_start_time_list = []
            unisono_stop_time_list = []

            for absolute_time, unisono_event in zip(
                sequential_unisono_event_to_convert.absolute_time_tuple,
                sequential_unisono_event_to_convert,
            ):
                unisono_event_duration = unisono_event.duration
                page_duration = unisono_event.page.duration
                rest_duration = unisono_event_duration - page_duration

                assert rest_duration >= 0

                # Insert time has to be equal to absolute time,
                # because if an interpolation doesn't have any
                # unisono in between, it will need the additional
                # time.
                # This is the reason why the following code has
                # been commented:
                #
                #   rest_half_duration = rest_duration / 2
                #   insert_time = absolute_time + rest_half_duration
                #
                insert_time = absolute_time

                unisono_start_time = insert_time
                unisono_stop_time = insert_time + page_duration

                if unisono_stop_time_list:
                    assert unisono_start_time >= unisono_stop_time_list[-1]
                if unisono_start_time_list:
                    assert unisono_stop_time > unisono_start_time_list[-1]

                unisono_start_time_list.append(unisono_start_time)
                unisono_stop_time_list.append(unisono_stop_time)

                for reader_index in unisono_event.reader_tuple:
                    simultaneous_event[reader_index].squash_in(
                        unisono_start_time, unisono_event.page
                    )

            return tuple(unisono_start_time_list), tuple(unisono_stop_time_list)

        def _insert_movement_events(
            self,
            duration: float,
            simultaneous_event: core_events.SimultaneousEvent,
            page_combination_tuple: tuple[tuple[dfc22_events.Page, ...], ...],
            movement_tuple: tuple[dfc22_events.SequentialUnisonoEvent.Movement, ...],
            unisono_start_time: tuple[float, ...],
            unisono_stop_time: tuple[float, ...],
        ):
            for start_time, stop_time in zip(unisono_start_time, unisono_stop_time):
                assert start_time < stop_time

            for movement, page_combination in zip(
                movement_tuple, page_combination_tuple
            ):
                start_time, end_time = (
                    unisono_stop_time[movement.unisono_event_left_index],
                    unisono_start_time[movement.unisono_event_right_index],
                )
                local_duration = (end_time - start_time) % duration
                movement_duration = sum(page.duration for page in page_combination)
                rest_duration = local_duration - movement_duration
                assert rest_duration >= 0
                rest_part_duration = rest_duration / (len(page_combination) + 1)
                sequential_event = simultaneous_event[movement.reader]
                insert_time = start_time + rest_part_duration
                initial_non_terminal_pair = (
                    movement.unisono_event_left.right_non_terminal_pair
                )
                for page in page_combination:
                    page = copy.deepcopy(page)
                    page.initial_non_terminal_pair = initial_non_terminal_pair
                    initial_non_terminal_pair = (
                        initial_non_terminal_pair + page.non_terminal_pair
                    )
                    insert_time = insert_time % duration
                    sequential_event.squash_in(insert_time, page)
                    insert_time += page.duration + rest_part_duration

        def _make_unprecise_simultaneous_event(
            self,
            sequential_unisono_event_to_convert: dfc22_events.SequentialUnisonoEvent,
            page_combination_tuple: tuple[tuple[dfc22_events.Page, ...], ...],
            movement_tuple: tuple[dfc22_events.SequentialUnisonoEvent.Movement, ...],
        ):
            duration = sequential_unisono_event_to_convert.duration
            simultaneous_event = core_events.SimultaneousEvent(
                [
                    core_events.SequentialEvent([core_events.SimpleEvent(duration)])
                    for _ in range(self._reader_count)
                ]
            )
            unisono_start_time, unisono_stop_time = self._insert_unisono_events(
                sequential_unisono_event_to_convert, simultaneous_event
            )
            self._insert_movement_events(
                duration,
                simultaneous_event,
                page_combination_tuple,
                movement_tuple,
                unisono_start_time,
                unisono_stop_time,
            )

            return simultaneous_event

        def convert(
            self,
            sequential_unisono_event_to_convert: dfc22_events.SequentialUnisonoEvent,
            movement_tuple: tuple[dfc22_events.SequentialUnisonoEvent.Movement, ...],
            page_combination_tuple_per_movement: tuple[
                tuple[tuple[dfc22_events.Page, ...], ...], ...
            ],
            page_combination_index_tuple: tuple[int, ...],
        ) -> core_events.SimultaneousEvent:
            page_combination_tuple = tuple(
                page_combination_tuple[page_combination_index]
                for page_combination_tuple, page_combination_index in zip(
                    page_combination_tuple_per_movement, page_combination_index_tuple
                )
            )
            self._set_unisono_events_duration(
                page_combination_tuple,
                sequential_unisono_event_to_convert,
                movement_tuple,
            )
            return self._make_unprecise_simultaneous_event(
                sequential_unisono_event_to_convert,
                page_combination_tuple,
                movement_tuple,
            )

    def _find_page_combination_index_tuple(
        self,
        movement_tuple: tuple[dfc22_events.SequentialUnisonoEvent.Movement, ...],
        page_combination_tuple_per_movement: tuple[
            tuple[tuple[dfc22_events.Page, ...], ...], ...
        ],
        max_page_combination_index_tuple: tuple[int, ...],
    ) -> tuple[int, ...]:
        return tuple(0 for _ in max_page_combination_index_tuple)

    def _convert_to_simultaneous_event(
        self,
        *args,
        **kwargs,
    ) -> core_events.SimultaneousEvent:
        return self.DataToSimultaneousEvent(self._reader_count).convert(*args, **kwargs)

    def convert(
        self, sequential_unisono_event_to_convert: dfc22_events.SequentialUnisonoEvent
    ) -> core_events.SimultaneousEvent:
        movement_tuple = tuple(sequential_unisono_event_to_convert.get_movement_set())
        page_combination_tuple_per_movement = tuple(
            self._page_combination_catalog[movement.as_non_terminal_pair]
            for movement in movement_tuple
        )
        max_page_combination_index_tuple = tuple(
            len(page_tuple) for page_tuple in page_combination_tuple_per_movement
        )
        page_combination_index_tuple = self._find_page_combination_index_tuple(
            movement_tuple,
            page_combination_tuple_per_movement,
            max_page_combination_index_tuple,
        )
        return self._convert_to_simultaneous_event(
            sequential_unisono_event_to_convert,
            movement_tuple,
            page_combination_tuple_per_movement,
            page_combination_index_tuple,
        )
