import abc
import typing

from mutwo import core_constants
from mutwo import core_events
from mutwo import core_utilities
from mutwo import dfc22_events
from mutwo import dfc22_parameters
from mutwo import music_parameters


__all__ = (
    "LanguageStructure",
    "PhonemeGroup",
    "Word",
    # "Sentence", "Paragraph", "Page"
)


def get_movement_sum(
    movement_sequence: typing.Sequence[music_parameters.JustIntonationPitch],
) -> music_parameters.JustIntonationPitch:
    return tuple(
        core_utilities.accumulate_from_n(
            movement_sequence, music_parameters.JustIntonationPitch("1/1")
        )
    )[-1]


class LanguageStructure(core_events.abc.Event):
    @property
    @abc.abstractmethod
    def uncertain_duration(self) -> dfc22_parameters.UncertainRange:
        """The duration of the structure"""

        raise NotImplementedError

    @property
    @abc.abstractmethod
    def uncertain_rest_duration(self) -> dfc22_parameters.UncertainRange:
        """The rest duration after the structure"""

        raise NotImplementedError

    @property
    @abc.abstractmethod
    def time_movement(self) -> music_parameters.JustIntonationPitch:
        """The summed movement of time."""

        raise NotImplementedError

    @property
    @abc.abstractmethod
    def pitch_movement(self) -> music_parameters.JustIntonationPitch:
        """The summed movement of pitch."""

        raise NotImplementedError


class PhonemeGroup(core_events.SimpleEvent, LanguageStructure):
    def __init__(
        self,
        uncertain_duration: dfc22_parameters.UncertainRange = dfc22_parameters.UncertainRange(
            0.2, 0.3
        ),
        phoneme_list: list[typing.Union[dfc22_parameters.XSAMPAPhoneme, str]] = ["a"],
        vowel_to_just_intonation_pitch_dict: typing.Optional[
            dict[dfc22_parameters.XSAMPAPhoneme, music_parameters.JustIntonationPitch]
        ] = None,
        consonant_to_just_intonation_pitch_dict: typing.Optional[
            dict[dfc22_parameters.XSAMPAPhoneme, music_parameters.JustIntonationPitch]
        ] = None,
    ):
        if not vowel_to_just_intonation_pitch_dict:
            vowel_to_just_intonation_pitch_dict = (
                dfc22_events.constants.DEFAULT_VOWEL_TO_JUST_INTONATION_PITCH_DICT
            )
        if not consonant_to_just_intonation_pitch_dict:
            consonant_to_just_intonation_pitch_dict = (
                dfc22_events.constants.DEFAULT_CONSONANT_TO_JUST_INTONATION_PITCH_DICT
            )
        self._vowel_to_just_intonation_pitch_dict = vowel_to_just_intonation_pitch_dict
        self._consonant_to_just_intonation_pitch_dict = (
            consonant_to_just_intonation_pitch_dict
        )
        self.uncertain_duration = uncertain_duration
        self.phoneme_list = [
            phoneme
            if isinstance(phoneme, dfc22_parameters.XSAMPAPhoneme)
            else dfc22_parameters.XSAMPAPhoneme(phoneme)
            for phoneme in phoneme_list
        ]

    @property
    def _parameter_to_print_tuple(self) -> tuple[str, ...]:
        """Return tuple of attribute names which shall be printed for repr."""
        return tuple(
            attribute
            for attribute in self._parameter_to_compare_tuple
            if attribute
            # Avoid too verbose and long attributes
            not in (
                "consonant_to_just_intonation_pitch_dict",
                "vowel_to_just_intonation_pitch_dict",
            )
        )

    @property
    def consonant_to_just_intonation_pitch_dict(
        self,
    ) -> dict[dfc22_parameters.XSAMPAPhoneme, music_parameters.JustIntonationPitch]:
        return self._consonant_to_just_intonation_pitch_dict

    @property
    def vowel_to_just_intonation_pitch_dict(
        self,
    ) -> dict[dfc22_parameters.XSAMPAPhoneme, music_parameters.JustIntonationPitch]:
        return self._vowel_to_just_intonation_pitch_dict

    @property
    def uncertain_duration(self) -> dfc22_parameters.UncertainRange:
        return self._uncertain_duration

    @uncertain_duration.setter
    def uncertain_duration(self, uncertain_duration: dfc22_parameters.UncertainRange):
        self._uncertain_duration = uncertain_duration

    @property
    def uncertain_rest_duration(self) -> dfc22_parameters.UncertainRange:
        """The rest duration after the structure"""
        return dfc22_parameters.UncertainRange(0.1, 0.2)

    @property
    def duration(self) -> core_constants.DurationType:
        return self.uncertain_duration.resolve()

    @duration.setter
    def duration(self, duration: core_constants.DurationType):
        self.uncertain_duration = dfc22_parameters.UncertainRange(
            duration * 0.985, duration * 1.025
        )

    @property
    def pitch_movement(self) -> music_parameters.JustIntonationPitch:
        return get_movement_sum(
            [
                self.vowel_to_just_intonation_pitch_dict[phoneme]
                for phoneme in self.phoneme_list
                if phoneme.is_vowel
            ]
        )

    @property
    def time_movement(self) -> music_parameters.JustIntonationPitch:
        return get_movement_sum(
            [
                self.consonant_to_just_intonation_pitch_dict[phoneme]
                for phoneme in self.phoneme_list
                if phoneme.is_consonant
            ]
        )


class Word(core_events.SequentialEvent[PhonemeGroup], LanguageStructure):
    def __str__(self):
        return f"{type(self).__name__}({''.join([str(word.phoneme_list)[1:-1] for word in self])})"

    @property
    def uncertain_duration(self) -> dfc22_parameters.UncertainRange:
        minima, maxima = 0, 0
        for phoneme_group in self:
            local_uncertain_duration = phoneme_group.uncertain_duration
            local_minima, local_maxima = (
                local_uncertain_duration.start,
                local_uncertain_duration.end,
            )
            minima += local_minima
            maxima += local_maxima
        return dfc22_parameters.UncertainRange(minima, maxima)

    @property
    def uncertain_rest_duration(self) -> dfc22_parameters.UncertainRange:
        """The rest duration after the structure"""
        return dfc22_parameters.UncertainRange(0.5, 1)

    @property
    def pitch_movement(self) -> music_parameters.JustIntonationPitch:
        return get_movement_sum(self.get_parameter("pitch_movement"))

    @property
    def time_movement(self) -> music_parameters.JustIntonationPitch:
        return get_movement_sum(self.get_parameter("time_movement"))
