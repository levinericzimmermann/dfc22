import dataclasses
import typing

from mutwo import core_constants
from mutwo import core_events
from mutwo import dfc22_events
from mutwo import dfc22_parameters

__all__ = ("UnisonoEvent", "SequentialUnisonoEvent")


class UnisonoEvent(core_events.SimpleEvent):
    def __init__(
        self,
        reader_tuple: tuple[int, ...],
        duration: core_constants.DurationType = 0,
        page: typing.Optional[dfc22_events.Page] = None,
        repetition_count: int = 1,
        non_terminal_pair: typing.Optional[dfc22_parameters.NonTerminalPair] = None,
    ):
        super().__init__(duration)
        self.reader_tuple = reader_tuple
        self.page = page
        self.repetition_count = repetition_count
        self.non_terminal_pair = non_terminal_pair

    @property
    def _parameter_to_print_tuple(self) -> tuple[str, ...]:
        """Return tuple of attribute names which shall be printed for repr."""
        return tuple(
            attribute
            for attribute in self._parameter_to_compare_tuple
            if attribute
            # Avoid too verbose and long attributes
            not in ("page",)
        )

    @property
    def right_non_terminal_pair(
        self,
    ) -> typing.Optional[dfc22_parameters.NonTerminalPair]:
        if self.non_terminal_pair:
            return self.non_terminal_pair + self.page.non_terminal_pair
        else:
            return None

    @property
    def page(self) -> dfc22_events.Page:
        return self._page

    @page.setter
    def page(self, page: typing.Optional[dfc22_events.Page]):
        self._page = page
        if page is not None:
            self.duration = page.duration


class SequentialUnisonoEvent(core_events.SequentialEvent[UnisonoEvent]):
    @dataclasses.dataclass(frozen=True)
    class Movement(object):
        reader: int

        unisono_event_left: UnisonoEvent
        unisono_event_right: UnisonoEvent

        unisono_event_left_index: int
        unisono_event_right_index: int

        def __hash__(self) -> int:
            return hash(
                (
                    self.reader,
                    self.unisono_event_left_index,
                    self.unisono_event_right_index,
                )
            )

        def __eq__(self, other: typing.Any):
            try:
                return hash(self) == hash(other)
            except Exception:
                return False

        @property
        def as_non_terminal_pair(
            self,
        ) -> typing.Optional[dfc22_parameters.NonTerminalPair]:
            try:
                non_terminal_pair_left, non_terminal_pair_right = (
                    self.unisono_event_left.right_non_terminal_pair,
                    self.unisono_event_right.non_terminal_pair,
                )
            except AttributeError:
                return None
            else:
                return non_terminal_pair_right - non_terminal_pair_left

        @property
        def distance(self) -> int:
            return abs(self.unisono_event_right - self.unisono_event_left)

        def __repr__(self) -> str:
            return (
                f"{type(self).__name__}"
                f"(reader={self.reader}, left_index={self.unisono_event_left_index}, "
                f"right_index={self.unisono_event_right_index})"
            )

    def get_movement_set(self) -> set[Movement]:
        movement_list = []
        for index, _ in enumerate(self):
            for reader_index_to_movement in self.get_movement_dict(index).values():
                for movement in reader_index_to_movement.values():
                    if movement not in movement_list:
                        movement_list.append(movement)
        return set(movement_list)

    def get_movement_dict(
        self, unisono_event_index: int
    ) -> dict[bool, dict[int, Movement]]:
        """
        Find all interpolations from unisono event to next unisono event
        where the reader appears.

        The dict has two entries:

            `True` -> for the movements from the UnisonoEvent to the future
            `False` -> for the movements from the past to the UnisonoEvent

        The nested dicts have the meaning:

            reader_index -> Movement
        """

        movement_dict = {True: {}, False: {}}
        unisono_event = self[unisono_event_index]

        future_unisono_event_tuple = tuple(
            self[unisono_event_index + 1 :] + self[:unisono_event_index]
        )
        future_unisono_event_index_tuple = tuple(
            range(unisono_event_index + 1, len(self))
        ) + tuple(range(unisono_event_index))

        past_unisono_event_tuple = tuple(reversed(future_unisono_event_tuple))
        past_unisono_event_index_tuple = tuple(
            reversed(future_unisono_event_index_tuple)
        )

        reader_index_to_find_tuple = unisono_event.reader_tuple

        for movement_direction, unisono_event_tuple, unisono_event_index_tuple in (
            (True, future_unisono_event_tuple, future_unisono_event_index_tuple),
            (False, past_unisono_event_tuple, past_unisono_event_index_tuple),
        ):
            reader_index_to_find_list = list(reader_index_to_find_tuple)
            for unisono_event_to_compare, unisono_event_to_compare_index in zip(
                unisono_event_tuple, unisono_event_index_tuple
            ):
                for reader_index in unisono_event_to_compare.reader_tuple:
                    if reader_index in reader_index_to_find_list:
                        unisono_event_pair = (unisono_event, unisono_event_to_compare)
                        unisono_index_pair = (
                            unisono_event_index,
                            unisono_event_to_compare_index,
                        )
                        if not movement_direction:
                            unisono_event_pair = tuple(reversed(unisono_event_pair))
                            unisono_index_pair = tuple(reversed(unisono_index_pair))
                        movement = self.Movement(
                            reader_index, *unisono_event_pair, *unisono_index_pair
                        )
                        movement_dict[movement_direction].update(
                            {reader_index: movement}
                        )
                        del reader_index_to_find_list[
                            reader_index_to_find_list.index(reader_index)
                        ]

        return movement_dict
