import typing

import quicktions as fractions

from mutwo import core_constants
from mutwo import core_converters
from mutwo import core_events
from mutwo import music_events

__all__ = ("SequentialEventToPulseBasedSequentialEvent",)


class SequentialEventToPulseBasedSequentialEvent(core_converters.abc.EventConverter):
    def __init__(
        self,
        simple_event_to_pulse: typing.Callable[
            [core_events.SimpleEvent], fractions.Fraction
        ] = core_converters.SimpleEventToAttribute("pulse", None),
    ):
        self._simple_event_to_pulse = simple_event_to_pulse

    def _convert_simple_event(
        self,
        simple_event_to_convert: core_events.SimpleEvent,
        _: core_constants.DurationType,
    ) -> tuple[core_events.SimpleEvent, ...]:
        pulse = self._simple_event_to_pulse(simple_event_to_convert)
        if pulse is not None:
            pulse = float(pulse)
            duration = simple_event_to_convert.duration
            pulse_count = int(duration / pulse)
            note_like_list = [
                music_events.NoteLike(pitch_list="1/1", volume=-6, duration=pulse)
                for _ in range(pulse_count)
            ]
            duration_difference = duration - sum(
                note_like.duration for note_like in note_like_list
            )
            if duration_difference and not note_like_list:
                assert duration_difference > 0
                note_like_list.append(
                    music_events.NoteLike(
                        pitch_list="1/1", volume=-2, duration=duration_difference
                    )
                )
            else:
                note_like_list[-1].duration += duration_difference
            for note_like in note_like_list[1:]:
                note_like.volume = -40
            return tuple(note_like_list)
        else:
            return (core_events.SimpleEvent(simple_event_to_convert.duration),)

    def convert(self, event_to_convert: core_events.abc.Event):
        pulse_based_sequential_event = core_events.SequentialEvent(
            self._convert_event(event_to_convert, 0)
        )
        try:
            assert round(pulse_based_sequential_event.duration, 2) == round(event_to_convert.duration, 2)
        except AssertionError:
            raise Exception(
                (
                    "unequal duration!"
                    f"pulse based: {pulse_based_sequential_event.duration}; "
                    f"original: {event_to_convert.duration}"
                )
            )
        return pulse_based_sequential_event
