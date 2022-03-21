import itertools
import os
import typing
import warnings
import uuid

import numpy as np
import moviepy

from mutwo import common_generators
from mutwo import core_constants
from mutwo import core_converters
from mutwo import core_events
from mutwo import core_utilities
from mutwo import dfc22_converters
from mutwo import dfc22_events
from mutwo import dfc22_parameters


__all__ = (
    "SequentialEventToVideo",
    "VideoPathSequenceToVideo",
    "AlphabetToNoiseGridVideo",
    "SequentialEventToLetterWriteVideo",
)


class ToVideo(object):
    def __init__(
        self,
        frames_per_second: int = 24,
        codec: str = "libx264",
    ):
        self._frames_per_second = frames_per_second
        self._codec = codec


class SequentialEventToVideo(ToVideo, core_converters.abc.EventConverter):
    def __init__(
        self,
        alphabet: dfc22_parameters.Alphabet,
        *args,
        simple_event_to_phoneme: typing.Callable[
            [core_events.SimpleEvent], typing.Optional[str]
        ] = core_converters.SimpleEventToAttribute("phoneme", "_"),
        **kwargs,
    ):
        ToVideo.__init__(self, *args, **kwargs)
        self._alphabet = alphabet
        self._simple_event_to_phoneme = simple_event_to_phoneme
        self._image_size = alphabet[0].image.size

    def _convert_simple_event(
        self,
        event_to_convert: typing.Union[
            core_events.SimpleEvent, dfc22_events.NoteLikeWithPhoneme
        ],
        _: core_constants.DurationType,
    ) -> tuple[moviepy.VideoClip]:
        phoneme_string = self._simple_event_to_phoneme(event_to_convert)
        phoneme = dfc22_parameters.XSAMPAPhoneme(phoneme_string)
        letter_tuple = self._alphabet.get_letter_tuple(phoneme)
        assert letter_tuple
        letter = letter_tuple[0]
        image_path = letter.image_path
        image_clip = moviepy.ImageClip(image_path, duration=event_to_convert.duration)
        return (image_clip,)

    def _add_image_path(self):
        for letter_index, letter in enumerate(self._alphabet):
            image_path = f".letter{letter_index}{uuid.uuid4()}.png"
            letter.image.save(image_path)
            letter.image_path = image_path

    def convert(self, event_to_convert: core_events.abc.Event, path: str):
        self._add_image_path()

        video_clip_tuple = self._convert_event(event_to_convert, 0)
        video_clip = moviepy.concatenate_videoclips(video_clip_tuple)
        video_clip.write_videofile(path, fps=self._frames_per_second, codec=self._codec)

        for letter in self._alphabet:
            os.remove(letter.image_path)


class VideoPathSequenceToVideo(ToVideo, core_converters.abc.Converter):
    def __init__(self, grid: tuple[int, int], size: tuple[int, int], *args, **kwargs):
        ToVideo.__init__(self, *args, **kwargs)
        self._grid = grid
        self._size = size
        self._video_x_size = int(self._size[0] / grid[0])
        self._video_y_size = int(self._size[1] / grid[1])
        self._video_count = grid[0] * grid[1]

    def _position_to_x_count_and_y_count(self, position: int) -> tuple[int, int]:
        x_count = position % self._grid[0]
        y_count = position // self._grid[0]
        return x_count, y_count

    def _x_count_and_y_count_to_absolute_position(
        self, x_count_and_y_count: tuple[int, int]
    ) -> tuple[int, int]:
        return (
            self._video_x_size * x_count_and_y_count[0],
            self._video_y_size * x_count_and_y_count[1],
        )

    def _find_video_clip_position_and_size(
        self, video_path_sequence_count: int
    ) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        position_list = []
        size_list = []
        grid_part_count_distribution = common_generators.euclidean(
            self._video_count, video_path_sequence_count
        )
        grid_part_count_distribution_accumulation = tuple(
            core_utilities.accumulate_from_zero(grid_part_count_distribution)
        )
        for start, stop, grid_part_count in zip(
            grid_part_count_distribution_accumulation,
            grid_part_count_distribution_accumulation[1:],
            grid_part_count_distribution,
        ):
            stop -= 1
            x_y_count_start = self._position_to_x_count_and_y_count(start)
            x_y_count_stop = self._position_to_x_count_and_y_count(stop)
            while x_y_count_stop[0] != x_y_count_start[0]:
                stop -= 1
                grid_part_count -= 1
                x_y_count_stop = self._position_to_x_count_and_y_count(stop)
            absolute_position = self._x_count_and_y_count_to_absolute_position(
                x_y_count_start
            )
            position_list.append(absolute_position)
            size_list.append(
                self._x_count_and_y_count_to_absolute_position((grid_part_count, 1))
            )
        return position_list, size_list

    def _make_video_clip(
        self,
        video_path_sequence: typing.Sequence[str],
        position_list: list[tuple[int, int]],
        size_list: list[tuple[int, int]],
    ):
        video_clip_list = []
        for video_path, size, position in zip(
            video_path_sequence, size_list, position_list
        ):
            local_video_clip = (
                # moviepy.VideoFileClip(video_path).resize(size).with_position(position)
                moviepy.VideoFileClip(video_path)
                .subclip(0, 60 * 20)
                .resize(size)
                .with_position(position)
            )
            video_clip_list.append(local_video_clip)

        background_clip = moviepy.ColorClip(
            self._size,
            color=(1, 1, 1),
            duration=max([video_clip.duration for video_clip in video_clip_list]),
        )

        return moviepy.CompositeVideoClip([background_clip] + video_clip_list)

    def convert(self, video_path_sequence: typing.Sequence[str], path: str):
        video_path_sequence_count = len(video_path_sequence)
        difference = self._video_count - video_path_sequence_count
        if difference < 0:
            video_path_sequence = video_path_sequence[:difference]
            warnings.warn(
                (
                    "Grid only support {self._video_count} videos! "
                    "Found {abs(difference)} too many video paths."
                )
            )
            video_path_sequence_count = len(video_path_sequence)

        position_list, size_list = self._find_video_clip_position_and_size(
            video_path_sequence_count
        )

        video_clip = self._make_video_clip(
            video_path_sequence, position_list, size_list
        )
        video_clip.write_videofile(path, fps=self._frames_per_second, codec=self._codec)


class AlphabetToNoiseGridVideo(ToVideo, core_converters.abc.Converter):
    def __init__(
        self,
        *args,
        letter_tuple_to_image: dfc22_converters.LetterTupleToImage = dfc22_converters.LetterTupleToImage(
            background_color="black",
            paper_canvas=dfc22_converters.PaperCanvas(1920, 1080),
            x_whitespace=20,
            y_whitespace=20,
            letter_height=135,
        ),
        seed: int = 100,
        frame_size_tuple=(1, 2, 2, 4, 3, 1, 3, 1, 2),
        **kwargs,
    ):
        ToVideo.__init__(self, *args, **kwargs)
        self._frame_size_tuple = frame_size_tuple
        self._letter_tuple_to_image = letter_tuple_to_image
        self._row_count = int(
            (
                letter_tuple_to_image._paper_canvas.y
                - (letter_tuple_to_image._y_margin * 2)
            )
            / (
                letter_tuple_to_image._letter_height
                + letter_tuple_to_image._y_whitespace
            )
        )
        self._random = np.random.default_rng(seed)

    def convert(
        self,
        alphabet_to_convert: dfc22_parameters.Alphabet,
        path: str,
        duration: float = 25,
    ):
        letter_width = self._letter_tuple_to_image._letter_height * (
            alphabet_to_convert[0].image.size[0] / alphabet_to_convert[0].image.size[1]
        )
        column_count = int(
            (self._letter_tuple_to_image._max_x - self._letter_tuple_to_image._x_margin)
            / (letter_width + self._letter_tuple_to_image._x_whitespace)
        )
        letter_count = self._row_count * column_count
        alphabet_count = len(alphabet_to_convert)
        letter_index_list = [0 for _ in range(letter_count)]
        frame_size_cycle = itertools.cycle(self._frame_size_tuple)
        image_path_list = []
        video_clip_list = []
        reached_duration: float = 0
        while reached_duration < duration:
            print("Progress:", round((reached_duration / duration) * 100, 2), "%")
            letter_tuple = tuple(
                alphabet_to_convert[letter_index] for letter_index in letter_index_list
            )
            image_path = f".noise_{uuid.uuid4()}.png"
            self._letter_tuple_to_image.convert(letter_tuple, image_path)
            image_path_list.append(image_path)
            frame_size = next(frame_size_cycle)
            image_clip_duration = frame_size / self._frames_per_second
            image_clip = moviepy.ImageClip(image_path, duration=image_clip_duration)
            video_clip_list.append(image_clip)
            for letter_to_change_index in self._random.choice(
                list(range(letter_count)),
                size=min((frame_size * 7, letter_count)),
                replace=False,
            ):
                new_letter_index = self._random.choice(
                    list(range(alphabet_count)), size=1
                )[0]
                letter_index_list[int(letter_to_change_index)] = int(new_letter_index)
            reached_duration += image_clip_duration
        video_clip = moviepy.concatenate_videoclips(video_clip_list)
        video_clip.write_videofile(path, fps=self._frames_per_second, codec=self._codec)
        for image_path in image_path_list:
            os.remove(image_path)


class SequentialEventToLetterWriteVideo(ToVideo, core_converters.abc.EventConverter):
    def __init__(
        self,
        alphabet: dfc22_parameters.Alphabet,
        *args,
        simple_event_to_phoneme: typing.Callable[
            [core_events.SimpleEvent], typing.Optional[str]
        ] = core_converters.SimpleEventToAttribute("phoneme", "_"),
        **kwargs,
    ):
        ToVideo.__init__(self, *args, **kwargs)
        self._alphabet = alphabet
        self._simple_event_to_phoneme = simple_event_to_phoneme
        self._image_size = alphabet[0].image.size

    def _convert_simple_event(
        self,
        event_to_convert: typing.Union[
            core_events.SimpleEvent, dfc22_events.NoteLikeWithPhoneme
        ],
        _: core_constants.DurationType,
    ) -> tuple[moviepy.VideoClip]:
        phoneme_string = self._simple_event_to_phoneme(event_to_convert)
        phoneme = dfc22_parameters.XSAMPAPhoneme(phoneme_string)
        letter_tuple = self._alphabet.get_letter_tuple(phoneme)
        assert letter_tuple
        letter = letter_tuple[0]
        image_path = letter.image_path
        image_clip = moviepy.ImageClip(image_path, duration=event_to_convert.duration)
        return (image_clip,)

    def _add_image_path(self):
        for letter_index, letter in enumerate(self._alphabet):
            image_path = f".letter{letter_index}{uuid.uuid4()}.png"
            letter.image.save(image_path)
            letter.image_path = image_path

    def convert(self, event_to_convert: core_events.abc.Event, path: str):
        self._add_image_path()

        video_clip_tuple = self._convert_event(event_to_convert, 0)
        video_clip = moviepy.concatenate_videoclips(video_clip_tuple)
        video_clip.write_videofile(path, fps=self._frames_per_second, codec=self._codec)

        for letter in self._alphabet:
            os.remove(letter.image_path)
