from mutwo import core_events
from mutwo import dfc22_converters
from mutwo import mbrola_converters
from mutwo import music_events

import dfc22


event_to_sound_file = mbrola_converters.EventToSpeakSynthesis()

for index, sequential_event in enumerate(dfc22.constants.SIMULTANEOUS_EVENT_WITH_NOTES):
    event_to_mixed_sound_file = dfc22_converters.EventToMixedSoundFile(
        f"builds/pages/{index}",
        event_to_sound_file,
        lambda event: isinstance(event, core_events.SequentialEvent)
        and isinstance(event[0], music_events.NoteLike),
    )

    event_to_mixed_sound_file.convert(sequential_event, f"builds/pages/{index}.wav")
