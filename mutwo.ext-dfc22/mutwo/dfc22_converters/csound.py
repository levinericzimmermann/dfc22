import concurrent.futures
import os
import typing
import uuid

from mutwo import core_constants
from mutwo import core_events
from mutwo import csound_converters


__all__ = ("EventToMixedSoundFile",)


class EventToMixedSoundFile(csound_converters.EventToSoundFile):
    class EventToCsoundScore(csound_converters.EventToCsoundScore):
        path_attribute_name = "path"

        def __init__(
            self,
            sound_file_directory_path: str,
            event_to_sound_file: typing.Callable[[core_events.abc.Event, str], None],
            shall_event_be_passed_to_generate_sound_file: typing.Callable[
                [core_events.abc.Event], bool
            ],
        ):
            super().__init__(
                p4=lambda simple_event: getattr(simple_event, self.path_attribute_name)
            )
            if not os.path.isdir(sound_file_directory_path):
                os.mkdir(sound_file_directory_path)

            self._sound_file_directory_path = sound_file_directory_path
            self._event_to_sound_file = event_to_sound_file
            self._shall_event_be_passed_to_generate_sound_file = (
                shall_event_be_passed_to_generate_sound_file
            )

        def _convert_event(
            self,
            event_to_convert: core_events.abc.Event,
            absolute_time: core_constants.DurationType,
        ) -> tuple[str, ...]:
            if self._shall_event_be_passed_to_generate_sound_file(event_to_convert):
                path = "{}/{}.wav".format(self._sound_file_directory_path, uuid.uuid4())
                self._event_to_sound_file(event_to_convert, path)
                event_to_convert = core_events.SimpleEvent(event_to_convert.duration)
                event_to_convert.path = path

            return super()._convert_event(event_to_convert, absolute_time)

    orchestra = """
instr 1
    asig diskin2 p4, 1, 0, 0
    out asig
endin
"""

    def __init__(self, *args, **kwargs):
        self._csound_orchestra_path = ".event_to_mixed_sound_file_{}.orc".format(
            uuid.uuid1()
        )
        super().__init__(
            self._csound_orchestra_path, self.EventToCsoundScore(*args, **kwargs)
        )

    def _make_orchestra(self):
        with open(self._csound_orchestra_path, "w") as csound_orchestra:
            csound_orchestra.write(self.orchestra)

    def _remove_orchestra(self):
        os.remove(self._csound_orchestra_path)

    def convert(self, *args, **kwargs):
        self._make_orchestra()
        return_value = super().convert(*args, **kwargs)
        self._remove_orchestra()
        return return_value
