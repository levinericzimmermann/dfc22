import abc
import typing
import warnings

from mutwo import core_constants
from mutwo import core_events
from mutwo import core_utilities
from mutwo import dfc22_events
from mutwo import dfc22_parameters
from mutwo import music_parameters


__all__ = (
    "LanguageStructure",
    "NestedLanguageStructure",
    "PhonemeGroup",
    "Word",
    "Sentence",
    "Paragraph",
    "Page",
)


def get_movement_sum(
    movement_sequence: typing.Sequence[music_parameters.JustIntonationPitch],
) -> music_parameters.JustIntonationPitch:
    return tuple(
        core_utilities.accumulate_from_n(
            movement_sequence, music_parameters.JustIntonationPitch("1/1")
        )
    )[-1]


class LanguageStructure(object):
    def __init__(
        self,
        uncertain_rest_duration: dfc22_parameters.UncertainRange = dfc22_parameters.UncertainRange(
            0.1, 0.2
        ),
        initial_non_terminal_pair: dfc22_parameters.NonTerminalPair = dfc22_parameters.NonTerminalPair(),
    ):
        self._uncertain_rest_duration = uncertain_rest_duration
        self.initial_non_terminal_pair = initial_non_terminal_pair

    @property
    @abc.abstractmethod
    def uncertain_duration(self) -> dfc22_parameters.UncertainRange:
        """The duration of the structure"""

        raise NotImplementedError

    @property
    def uncertain_rest_duration(self) -> dfc22_parameters.UncertainRange:
        """The rest duration after the structure"""
        return self._uncertain_rest_duration

    @uncertain_rest_duration.setter
    def uncertain_rest_duration(
        self, uncertain_rest_duration: dfc22_parameters.UncertainRange
    ):
        self._uncertain_rest_duration = uncertain_rest_duration

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

    @property
    @abc.abstractmethod
    def as_xsampa_text(self) -> str:
        raise NotImplementedError

    @property
    def non_terminal_pair(self) -> dfc22_parameters.NonTerminalPair:
        return dfc22_parameters.NonTerminalPair(
            consonant=self.time_movement, vowel=self.pitch_movement
        )


class PhonemeGroup(core_events.SimpleEvent, LanguageStructure):
    def __init__(
        self,
        uncertain_duration: typing.Optional[dfc22_parameters.UncertainRange] = None,
        phoneme_list: list[typing.Union[dfc22_parameters.XSAMPAPhoneme, str]] = ["a"],
        vowel_to_just_intonation_pitch_dict: typing.Optional[
            dict[dfc22_parameters.XSAMPAPhoneme, music_parameters.JustIntonationPitch]
        ] = None,
        consonant_to_just_intonation_pitch_dict: typing.Optional[
            dict[dfc22_parameters.XSAMPAPhoneme, music_parameters.JustIntonationPitch]
        ] = None,
        uncertain_rest_duration: typing.Optional[
            dfc22_parameters.UncertainRange
        ] = None,
    ):
        if uncertain_duration is None:
            uncertain_duration = (
                dfc22_events.configurations.DEFAULT_UNCERTAIN_DURATION_FOR_PHONEME_GROUP
            )
        if uncertain_rest_duration is None:
            uncertain_rest_duration = (
                dfc22_events.configurations.DEFAULT_UNCERTAIN_REST_DURATION_FOR_PHONEME_GROUP
            )
        LanguageStructure.__init__(self, uncertain_rest_duration)
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

    @staticmethod
    def _get_center(start: float, stop: float) -> float:
        return ((stop - start) / 2) + start

    @property
    def duration(self) -> core_constants.DurationType:
        return self._get_center(
            self.uncertain_duration.start, self.uncertain_duration.end
        ) + self._get_center(
            self.uncertain_rest_duration.start, self.uncertain_rest_duration.end
        )

    @duration.setter
    def duration(self, duration: core_constants.DurationType):
        warnings.warn(
            (
                "You set the duration of phoneme group. "
                "This may lead to unexpected results."
            )
        )
        self.uncertain_duration = dfc22_parameters.UncertainRange(
            duration, duration * 1.0001
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

    @property
    def as_xsampa_text(self) -> str:
        return "".join([phoneme.phoneme for phoneme in self.phoneme_list])


T = typing.TypeVar("T", bound=LanguageStructure)


class NestedLanguageStructure(
    core_events.SequentialEvent, typing.Generic[T], LanguageStructure
):
    xsampa_text_separator = " "

    def __init__(
        self,
        *args,
        uncertain_rest_duration: dfc22_parameters.UncertainRange,
        **kwargs,
    ):
        LanguageStructure.__init__(self, uncertain_rest_duration)
        super().__init__(*args, **kwargs)

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
    def pitch_movement(self) -> music_parameters.JustIntonationPitch:
        return get_movement_sum([event.pitch_movement for event in self])

    @property
    def time_movement(self) -> music_parameters.JustIntonationPitch:
        return get_movement_sum([event.time_movement for event in self])

    @property
    def as_xsampa_text(self) -> str:
        return self.xsampa_text_separator.join([event.as_xsampa_text for event in self])


class Word(NestedLanguageStructure[PhonemeGroup]):
    xsampa_text_separator = ""

    def __init__(
        self,
        *args,
        uncertain_rest_duration: typing.Optional[
            dfc22_parameters.UncertainRange
        ] = None,
        **kwargs,
    ):
        if uncertain_rest_duration is None:
            uncertain_rest_duration = (
                dfc22_events.configurations.DEFAULT_UNCERTAIN_REST_DURATION_FOR_WORD
            )
        super().__init__(
            *args, uncertain_rest_duration=uncertain_rest_duration, **kwargs
        )

    def __str__(self):
        return (
            f"{type(self).__name__}"
            f"({''.join([str(word.phoneme_list)[1:-1] for word in self])})"
        )

    @property
    def uncertain_rest_duration(self) -> dfc22_parameters.UncertainRange:
        """The rest duration after the structure"""

        return dfc22_parameters.UncertainRange(0.5, 1)


class Sentence(NestedLanguageStructure[Word]):
    xsampa_text_separator = " "

    def __init__(
        self,
        *args,
        uncertain_rest_duration: typing.Optional[
            dfc22_parameters.UncertainRange
        ] = None,
        **kwargs,
    ):
        if uncertain_rest_duration is None:
            uncertain_rest_duration = (
                dfc22_events.configurations.DEFAULT_UNCERTAIN_REST_DURATION_FOR_SENTENCE
            )
        super().__init__(
            *args, uncertain_rest_duration=uncertain_rest_duration, **kwargs
        )


class Paragraph(NestedLanguageStructure[Sentence]):
    xsampa_text_separator = "! "

    def __init__(
        self,
        *args,
        uncertain_rest_duration: typing.Optional[
            dfc22_parameters.UncertainRange
        ] = None,
        **kwargs,
    ):
        if uncertain_rest_duration is None:
            uncertain_rest_duration = (
                dfc22_events.configurations.DEFAULT_UNCERTAIN_REST_DURATION_FOR_PARAGRAPH
            )
        super().__init__(
            *args, uncertain_rest_duration=uncertain_rest_duration, **kwargs
        )

    @property
    def as_xsampa_text(self) -> str:
        return (
            self.xsampa_text_separator.join([event.as_xsampa_text for event in self])
            + self.xsampa_text_separator
        )


class Page(NestedLanguageStructure[Paragraph]):
    xsampa_text_separator = "\n\n"

    def __init__(
        self,
        *args,
        uncertain_rest_duration: typing.Optional[
            dfc22_parameters.UncertainRange
        ] = None,
        **kwargs,
    ):
        if uncertain_rest_duration is None:
            uncertain_rest_duration = (
                dfc22_events.configurations.DEFAULT_UNCERTAIN_REST_DURATION_FOR_PAGE
            )
        super().__init__(
            *args, uncertain_rest_duration=uncertain_rest_duration, **kwargs
        )

    @property
    def as_xsampa_text(self) -> str:
        xsampa_text = super().as_xsampa_text
        return "".join(["\t" + line + "\n" for line in xsampa_text.split("\n")])

    def __hash__(self) -> int:
        # UNSAFE HASH!
        return hash(self.as_xsampa_text)
