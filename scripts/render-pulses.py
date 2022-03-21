from mutwo import dfc22_converters

import dfc22


sequential_event_to_pulse_based_sequential_event = (
    dfc22_converters.SequentialEventToPulseBasedSequentialEvent()
)
event_to_sound_file = dfc22_converters.EventToPulseSoundFile()

for index, sequential_event in enumerate(dfc22.constants.SIMULTANEOUS_EVENT_WITH_NOTES):
    pulse_based_sequential_event = (
        sequential_event_to_pulse_based_sequential_event.convert(sequential_event)
    )
    event_to_mixed_sound_file = event_to_sound_file.convert(
        pulse_based_sequential_event,
        f"builds/pulses/{index}.wav",
    )
