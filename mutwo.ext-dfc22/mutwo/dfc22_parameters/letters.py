"""Design letters from geometric forms"""


import abc
import dataclasses
import math
import typing
import uuid

from PIL import Image
import geometer
import qahirah

try:
    import quicktions as fractions
except ImportError:
    import fractions

from mutwo import core_events
from mutwo import dfc22_parameters

__all__ = (
    "LetterElement",
    "Polygon",
    "Triangle",
    "Quad",
    "Pentagon",
    "Hexagon",
    "Ellipsis",
    "LetterCanvas",
    "Letter",
)


def degree_to_radian(degree: float):
    return (degree / 180) * math.pi


class LetterCanvas(object):
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
        self._surface = qahirah.ImageSurface.create(qahirah.CAIRO.FORMAT_A8, (x, y))

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def center(self) -> tuple[float, float]:
        return (self.x / 2, self.y / 2)

    @property
    def ratio(self) -> fractions.Fraction:
        return fractions.Fraction(self.x / self.y)

    @property
    def surface(self) -> qahirah.ImageSurface:
        return self._surface


@dataclasses.dataclass()
class LetterElement(abc.ABC):
    """Basic class for letter elements.

    :param x_displacement: Value between -1 to +1. +/-1 means
        the centroid of the element is on the horizontal edge.
    :param y_displacement: Value between -1 to +1. +/-1 means
        the centroid of the element is on the vertical edge.
    :param thickness: Thickness of draw line.
    :param angle: Angle how much element is displaced.
        Default to 0. Value from 0 to 360
    """

    x_displacement: float = 0
    y_displacement: float = 0
    thickness: float = 0
    angle: float = 0

    @abc.abstractmethod
    def draw(self, letter_canvas: LetterCanvas):
        raise NotImplementedError


class Polygon(LetterElement, geometer.Polygon):
    def __init__(
        self,
        *args,
        point_sequence: typing.Sequence[geometer.Point],
        # `True` if side should be drawn, `False` if it should be ignored
        is_side_active_sequence: typing.Optional[typing.Sequence[bool]] = None,
        # 1 is max round, 0 is no round
        round_corner_strength_sequence: typing.Optional[typing.Sequence[float]] = None,
        # The length of the longest line. A value from 0 - 1 where
        #  1 == shortest side of canvas
        max_length: float = 0.5,
        **kwargs,
    ):

        if is_side_active_sequence is None:
            is_side_active_sequence = [True for _ in range(self.n_sides)]
        if round_corner_strength_sequence is None:
            round_corner_strength_sequence = [0 for _ in range(self.n_sides)]

        # sanity check
        for data_sequence in (
            is_side_active_sequence,
            round_corner_strength_sequence,
            point_sequence,
        ):
            assert len(data_sequence) == self.n_sides

        LetterElement.__init__(self, *args, **kwargs)
        geometer.Polygon.__init__(self, *point_sequence)

        self._is_side_active_tuple = tuple(is_side_active_sequence)
        self._round_corner_strength_tuple = tuple(round_corner_strength_sequence)
        self._max_length = max_length

    @classmethod
    def from_angles_and_lengths(
        cls,
        *args,
        # Scale angle size between two sides (not exact angle like
        # 180 degree, but only a ratio e.g. = (1, 1, 0.5)
        # -> means the first two angles are of equal size and the last
        # one is slightly smaller
        angle_proportion_sequence: typing.Optional[typing.Sequence[float]] = None,
        # The length proportion sequence should be two elements
        # shorter than n_sides. The length is also only proportional.
        # Later the longest side will be mapped to fit to `max_length`.
        length_proportion_sequence: typing.Optional[typing.Sequence[float]] = None,
        rotation_angle: float = 0,
        **kwargs,
    ):
        """Alternative constructor (from angles and side length instead from points)"""

        # syntactic sugar
        if angle_proportion_sequence is None:
            angle_proportion_sequence = [1 for _ in range(cls.n_sides)]
        if length_proportion_sequence is None:
            length_proportion_sequence = [1 for _ in range(cls.n_sides - 2)]

        # sanity check
        assert len(angle_proportion_sequence) == cls.n_sides
        assert len(length_proportion_sequence) == cls.n_sides - 2

        # we calculate the points so that they fit to the expected
        # form from the angles which we passed
        point_tuple = cls._angles_and_lenghts_to_point_tuple(
            angle_proportion_sequence, length_proportion_sequence
        )

        # now we have to move our point so that the center is (0, 0)
        point_tuple = Polygon._centralise_point_tuple(point_tuple)

        # last but not least we have to rotate the whole object by the
        # 'rotation_angle' argument
        point_tuple = Polygon._rotate_point_tuple(point_tuple, rotation_angle)

        # finally we can return our new object by calling the
        # default class constructor
        return cls(*args, point_sequence=point_tuple, **kwargs)

    @classmethod
    def _angles_and_lenghts_to_point_tuple(
        cls,
        angle_proportion_sequence: typing.Sequence[float],
        length_proportion_sequence: typing.Sequence[float],
    ) -> tuple[geometer.Point, ...]:
        angle_tuple = cls._angle_proportion_sequence_to_angle_tuple(
            angle_proportion_sequence
        )
        proportional_point_list = cls._angle_tuple_and_length_proportional_sequence_to_proportional_point_tuple(
            angle_tuple, length_proportion_sequence
        )
        return proportional_point_list

    @classmethod
    def _angle_proportion_sequence_to_angle_tuple(
        cls, angle_proportion_sequence: typing.Sequence[float]
    ) -> tuple[float, ...]:
        scalar_value = cls.interior_angle_sum / sum(angle_proportion_sequence)
        angle_tuple = tuple(
            scalar_value * angle_proportion
            for angle_proportion in angle_proportion_sequence
        )
        return angle_tuple

    @staticmethod
    def _find_next_point(
        previous_segment: geometer.Segment, angle: float, length_proportion: float
    ) -> geometer.Point:
        # we get interior angle, but we need exterior angle
        angle = - (180 - angle)
        # we get degree, but we need radian
        angle = degree_to_radian(angle)
        rotation_transformation = geometer.rotation(angle)
        scale_factor = length_proportion / previous_segment.length
        scale_transformation = geometer.scaling((scale_factor, scale_factor))
        normalization_transformation = geometer.translation(
            *[-n for n in previous_segment.vertices[0].normalized_array[:2]]
        )
        normalized_segment = normalization_transformation.apply(previous_segment)
        movement_transformation = geometer.translation(
            *previous_segment.vertices[1].normalized_array[:2]
        )
        new_segment = movement_transformation.apply(
            scale_transformation.apply(
                rotation_transformation.apply(normalized_segment)
            )
        )
        # sanity check
        assert new_segment.vertices[0] == previous_segment.vertices[-1]
        return new_segment.vertices[-1]

    @staticmethod
    def _centralise_point_tuple(
        point_tuple: tuple[geometer.Point, ...]
    ) -> tuple[geometer.Point, ...]:
        polygon = geometer.Polygon(*point_tuple)
        centroid = polygon.centroid
        centralise = geometer.translation(-centroid[0], -centroid[1])
        return tuple(centralise.apply(polygon).vertices)

    @staticmethod
    def _rotate_point_tuple(
        point_tuple: tuple[geometer.Point, ...], rotation_angle: float
    ) -> tuple[geometer.Point, ...]:
        rotation = geometer.rotation(degree_to_radian(rotation_angle))
        return tuple(rotation.apply(geometer.Polygon(*point_tuple)).vertices)

    @classmethod
    def _angle_tuple_and_length_proportional_sequence_to_proportional_point_tuple(
        cls,
        angle_tuple: tuple[float, ...],
        length_proportion_sequence: typing.Sequence[float],
    ) -> tuple[geometer.Point, ...]:
        point_list = [
            geometer.Point(0, 0),
            geometer.Point(-length_proportion_sequence[0], 0),
        ]
        for length_proportion, angle in zip(
            length_proportion_sequence[1:], angle_tuple
        ):
            point_list.append(
                Polygon._find_next_point(
                    geometer.Segment(point_list[-2], point_list[-1]),
                    angle,
                    length_proportion,
                )
            )

        # sanity check
        assert len(point_list) == cls.n_sides - 1

        # Now we have to figure out the last missing point.
        # We simply make two dummy points at the known angle
        # to the already defined lines. We draw two lines, one
        # to each dummy point and we check where the two lines
        # are meeting. Than we know where our last point is.
        line_list = []
        for point0, point1, angle in (
            (point_list[-2], point_list[-1], angle_tuple[-2]),
            (point_list[1], point_list[0], -angle_tuple[-1]),
        ):
            test_point = Polygon._find_next_point(
                geometer.Segment(point0, point1), angle, 1
            )
            test_line = geometer.Line(point1, test_point)
            line_list.append(test_line)

        point_list.append(geometer.meet(*line_list))

        return tuple(point_list)

    @classmethod
    @property
    def interior_angle_sum(cls) -> float:
        return (cls.n_sides - 2) * 180

    @property
    def is_side_active_tuple(self) -> tuple[bool, ...]:
        return self._is_side_active_tuple

    @property
    def round_corner_strength_tuple(self) -> tuple[float, ...]:
        return self._round_corner_strength_tuple

    @property
    def max_length(self) -> float:
        return self._max_length

    @classmethod
    @property
    @abc.abstractmethod
    def n_sides(cls) -> int:
        raise NotImplementedError

    def draw(self, letter_canvas: LetterCanvas):
        # SKALIERUNG DER LAENGEN ANGABEN:
        #   "1" == komplette laenge der kuerzeren seite des canvas
        #           -> die skalierung ist fuer x und y gleich, also der faktor wird
        #              gleich angewendet
        # +

        # OKAYYY
        # das funktioniert sooo...
        # (1) alle punkte ausrechnen (kannst du einfach ueber die wege und die winkel berechnen)
        #       -> dabei davon ausgehen dass die erste linie unten 90grad gerade ist
        # (2) die mitte von all diesen punkten ausrechnen : das ist auch die wirkliche mitte
        #      - vielleicht kannst du online nach formel suchen, mit der man von x punkten die mitte berechnet
        # (3) daraufhin alle punkte skalieren auf
        raise NotImplementedError


class Triangle(Polygon):
    @classmethod
    @property
    def n_sides(cls):
        return 3


class Quad(Polygon):
    @classmethod
    @property
    def n_sides(cls):
        return 4


class Pentagon(Polygon):
    @classmethod
    @property
    def n_sides(cls):
        return 5


class Hexagon(Polygon):
    @classmethod
    @property
    def n_sides(cls):
        return 6


class Ellipsis(LetterElement):
    def __init__(
        self,
        *args,
        activity_sequential_event: typing.Optional[
            core_events.SequentialEvent[core_events.SimpleEvent]
        ] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.activity_sequential_event = activity_sequential_event


@dataclasses.dataclass()
class Letter(dfc22_parameters.abc.Sign):
    letter_canvas: LetterCanvas
    letter_element_list: list[LetterElement]
    _png_path: typing.Optional[str] = None

    def _paint(self):
        for letter in self.letter_element_list:
            letter.draw(self.letter_canvas)
        png_file_name = f".mutwo_ext_filename_{uuid.uuid4()}.png"
        self._png_path = png_file_name
        self.letter_canvas.surface.write_to_png_file(png_file_name)

    @property
    def image(self) -> Image.Image:
        if self._png_path is None:
            self._paint()
            return self.image
        return Image.open(self._png_path)

    @property
    def phoneme_list(self):
        pass
