import typing

import numpy as np

from mutwo import core_converters
from mutwo import core_constants
from mutwo import core_events
from mutwo import dfc22_events
from mutwo import dfc22_parameters
from mutwo import music_parameters


__all__ = (
    "WordToSequentialEvent",
    "SentenceToSequentialEvent",
    "prepare_word_for_isis",
)


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
