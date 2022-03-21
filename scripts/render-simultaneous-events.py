from mutwo import core_events
from mutwo import dfc22_converters
from mutwo import isis_converters
from mutwo import mbrola_converters
from mutwo import music_events

import dfc22


def render_mbrola():
    event_to_sound_file = mbrola_converters.EventToSpeakSynthesis()

    for index, sequential_event in enumerate(
        dfc22.constants.SIMULTANEOUS_EVENT_WITH_NOTES
    ):
        event_to_mixed_sound_file = dfc22_converters.EventToMixedSoundFile(
            f"builds/pages/{index}",
            event_to_sound_file,
            lambda event: isinstance(event, core_events.SequentialEvent)
            and isinstance(event[0], music_events.NoteLike),
        )

        event_to_mixed_sound_file.convert(sequential_event, f"builds/pages/{index}.wav")


def render_isis():
    event_to_sound_file = isis_converters.EventToSingingSynthesis(
        isis_converters.EventToIsisScore(),
        "--cfg_synth etc/isis-cfg-synth.cfg",
        "--cfg_style etc/isis-cfg-style.cfg",
        "--seed 100",
    )

    for index, sequential_event in enumerate(
        dfc22.constants.SIMULTANEOUS_EVENT_WITH_ISIS_FRIENDLY_NOTES
    ):
        event_to_mixed_sound_file = dfc22_converters.EventToMixedSoundFile(
            f"builds/isis-pages/{index}",
            event_to_sound_file,
            lambda event: isinstance(event, core_events.SequentialEvent)
            and isinstance(event[0], music_events.NoteLike),
        )

        event_to_mixed_sound_file.convert(
            sequential_event[:30], f"builds/isis-pages/{index}.wav"
        )


if __name__ == "__main__":
    render_mbrola()
    render_isis()
