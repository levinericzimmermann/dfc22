"""Design letters from geometric forms"""


import abc
import dataclasses
import os
import math
import typing

from PIL import Image
import geometer
import qahirah

try:
    import quicktions as fractions
except ImportError:
    import fractions

from mutwo import core_events
from mutwo import core_utilities
from mutwo import dfc22_parameters

__all__ = (
    "LetterElement",
    "Polygon",
    "Triangle",
    "Quad",
    "Pentagon",
    "Hexagon",
    "Ellipsis",
    "Circle",
    "LetterCanvas",
    "Letter",
)


class LetterCanvas(object):
    def __init__(self, x: float = 800, y: float = 800):
        self._x = x
        self._y = y
        self._surface = qahirah.ImageSurface.create(qahirah.CAIRO.FORMAT_ARGB32, (x, y))

        # Make white background
        context = qahirah.Context.create(self.surface)
        context.source_colour = qahirah.Colour.x11["white"]
        context.paint()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(x = {self.x}, y = {self.y}"

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
    :param thickness: Thickness of draw_on line.
    :param color: Color of line.
    :param angle: Angle how much element is displaced.
        Default to 0. Value from 0 to 360
    """

    x_displacement: float = 0
    y_displacement: float = 0
    thickness: float = 15
    color: qahirah.Colour = qahirah.Colour.x11["black"]
    angle: float = 0

    @staticmethod
    def _displacement_value_to_displacement_percentage(
        displacement_value: float,
    ) -> float:
        return float(core_utilities.scale(displacement_value, -1, 1, 0, 1))

    def get_centroid(self, letter_canvas: LetterCanvas) -> geometer.Point:
        position_list = []
        for size, displacement in (
            (letter_canvas.x, self.x_displacement),
            (letter_canvas.y, self.y_displacement),
        ):
            position_list.append(
                size
                * LetterElement._displacement_value_to_displacement_percentage(
                    displacement
                )
            )
        return geometer.Point(*position_list)

    @abc.abstractmethod
    def draw_on(self, letter_canvas: LetterCanvas):
        raise NotImplementedError


class Polygon(LetterElement, geometer.Polygon):
    def __init__(
        self,
        *args,
        point_sequence: typing.Sequence[geometer.Point],
        # `True` if side should be draw_onn, `False` if it should be ignored
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
        self._length_proportion_tuple = tuple(
            geometer.dist(point0, point1)
            for point0, point1 in zip(
                point_sequence, point_sequence[1:] + point_sequence[:1]
            )
        )

    def __str__(self) -> str:
        return (
            f"{type(self).__name__}(length_proportion_tuple = {self.length_proportion_tuple}, "
            f"is_side_active_tuple = {self.is_side_active_tuple}, "
            f"round_corner_strength_tuple = {self.round_corner_strength_tuple}, "
            f"max_length = {self.max_length})"
        )

    def __repr__(self) -> str:
        return str(self)

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
        angle = -(180 - angle)
        # we get degree, but we need radian
        angle = math.radians(angle)
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
        point_tuple: tuple[geometer.Point, ...],
        center: geometer.Point = geometer.Point(0, 0),
    ) -> tuple[geometer.Point, ...]:
        polygon = geometer.Polygon(*point_tuple)
        centroid = polygon.centroid
        centralise = geometer.translation(
            -centroid.normalized_array[0] + center.normalized_array[0],
            -centroid.normalized_array[1] + center.normalized_array[1],
        )
        return tuple(centralise.apply(polygon).vertices)

    @staticmethod
    def _rotate_point_tuple(
        point_tuple: tuple[geometer.Point, ...], rotation_angle: float
    ) -> tuple[geometer.Point, ...]:
        rotation = geometer.rotation(math.radians(rotation_angle))
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
        # to the already defined lines. We draw_on two lines, one
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

    @property
    def length_proportion_tuple(self) -> tuple[float, ...]:
        return self._length_proportion_tuple

    @classmethod
    @property
    @abc.abstractmethod
    def n_sides(cls) -> int:
        raise NotImplementedError

    def _get_scaled_point_tuple(self, letter_canvas: LetterCanvas):
        length_of_shortest_side = min(letter_canvas.x, letter_canvas.y)
        max_side_length = length_of_shortest_side * self.max_length
        max_length_proportion = max(self.length_proportion_tuple)
        scale_factor = max_side_length / max_length_proportion
        scale_transformation = geometer.scaling((scale_factor, scale_factor))
        scaled_polygon = scale_transformation.apply(self)
        return tuple(scaled_polygon.vertices)

    def _get_adjusted_point_tuple(self, letter_canvas: LetterCanvas):
        return Polygon._centralise_point_tuple(
            self._get_scaled_point_tuple(letter_canvas),
            self.get_centroid(letter_canvas),
        )

    # #################################### #
    #  helper methods for drawing          #
    # #################################### #

    @staticmethod
    def _point_to_coordinate_tuple(point: geometer.Point) -> tuple[float, float]:
        x, y, *_ = point.normalized_array
        return float(x), float(y)

    @staticmethod
    def _draw_line(
        context: qahirah.Context,
        point0: geometer.Point,
        point1: geometer.Point,
        last_side_was_active: bool,
    ):
        x0, y0 = Polygon._point_to_coordinate_tuple(point0)
        x1, y1 = Polygon._point_to_coordinate_tuple(point1)
        if not last_side_was_active:
            context.move_to((x0, y0))
        context.line_to((x1, y1))

    @staticmethod
    def _draw_point_tuple_except_last_line(
        context: qahirah.Context,
        point_tuple: tuple[geometer.Point, ...],
        is_side_active_tuple: tuple[bool, ...],
    ) -> bool:
        last_side_was_active = False
        for point0, point1, is_side_active in zip(
            point_tuple,
            point_tuple[1:],
            is_side_active_tuple,
        ):
            if is_side_active:
                Polygon._draw_line(context, point0, point1, last_side_was_active)
                last_side_was_active = True
            else:
                last_side_was_active = False
        return last_side_was_active

    @staticmethod
    def _draw_last_line(
        context: qahirah.Context,
        point_tuple: tuple[geometer.Point, ...],
        is_side_active_tuple: tuple[bool, ...],
        last_side_was_active: bool,
    ):
        if is_side_active_tuple[-1]:
            if all(is_side_active_tuple):
                context.close_path()
            else:
                Polygon._draw_line(
                    context,
                    point_tuple[-1],
                    point_tuple[0],
                    last_side_was_active,
                )

    def _sort_point_tuple_and_is_side_active_tuple(
        self, point_tuple: tuple[geometer.Point, ...]
    ) -> tuple[tuple[geometer.Point, ...], tuple[bool, ...]]:
        """Round robin to avoid problematic construct.

        If is_side_active_tuple has the following structure:

            (True, ..., False, True)

        it is problematic, because when the last line goes to
        the first line it neither can call `context.close_path()`
        (because then the polygon form would change) and it also
        can't draw a line to the start point, because we would
        get ugly artifacts because the two lines can't meet
        for 100% precision.
        """

        is_side_active_tuple = self.is_side_active_tuple
        if not all(is_side_active_tuple):
            point_tuple_permutation = core_utilities.cyclic_permutations(point_tuple)
            is_side_active_tuple_permutation = core_utilities.cyclic_permutations(
                is_side_active_tuple
            )

            point_tuple = next(point_tuple_permutation)
            is_side_active_tuple = next(is_side_active_tuple_permutation)

            while is_side_active_tuple[0] and is_side_active_tuple[-1]:
                try:
                    point_tuple = next(point_tuple_permutation)
                    is_side_active_tuple = next(is_side_active_tuple_permutation)
                except StopIteration:
                    break

        return point_tuple, is_side_active_tuple

    def draw_on(self, letter_canvas: LetterCanvas):
        """Draws polygon element on letter canvas."""

        # Adjust polygon to letter canvas (scale and move)
        (
            point_tuple,
            is_side_active_tuple,
        ) = self._sort_point_tuple_and_is_side_active_tuple(
            self._get_adjusted_point_tuple(letter_canvas)
        )

        context = qahirah.Context.create(letter_canvas.surface)
        # TODO(apply round_corner_strength_tuple!)
        last_side_was_active = Polygon._draw_point_tuple_except_last_line(
            context, point_tuple, is_side_active_tuple
        )
        Polygon._draw_last_line(
            context,
            point_tuple,
            is_side_active_tuple,
            last_side_was_active,
        )
        context.source_colour = self.color
        context.line_width = self.thickness
        context.stroke()


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


class Circle(LetterElement):
    _circle_maxima = 2 * math.pi

    def __init__(
        self,
        *args,
        activity_tuple_sequence: typing.Sequence[tuple[float, bool]] = ((1, True),),
        radius_proportion: float = 0.5,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._activity_tuple_sequence = activity_tuple_sequence
        self.radius_proportion = radius_proportion

    def _draw_arc_parts(
        self,
        context: qahirah.Context,
        centre: tuple[float, float],
        radius: float,
        summed_length_proportion: float,
    ):
        position_percentage = 0
        for length_proportion, is_active in self._activity_tuple_sequence:
            new_position_percentage = position_percentage + (
                length_proportion / summed_length_proportion
            )
            if is_active:
                start_radian, end_radian = (
                    core_utilities.scale(position, 0, 1, 0, self._circle_maxima)
                    for position in (position_percentage, new_position_percentage)
                )
                context.arc(centre, radius, start_radian, end_radian, 0)

            position_percentage = new_position_percentage

    def draw_on(self, letter_canvas: LetterCanvas):
        """Draws circle element on letter canvas."""

        centre = Polygon._point_to_coordinate_tuple(self.get_centroid(letter_canvas))
        radius = self.radius_proportion * min((letter_canvas.x, letter_canvas.y))

        length_proportion_tuple, _ = zip(*self._activity_tuple_sequence)
        summed_length_proportion = sum(length_proportion_tuple)
        context = qahirah.Context.create(letter_canvas.surface)
        self._draw_arc_parts(context, centre, radius, summed_length_proportion)

        context.source_colour = self.color
        context.line_width = self.thickness
        context.stroke()


class Letter(dfc22_parameters.abc.Sign):
    def __init__(
        self,
        letter_canvas: LetterCanvas,
        letter_element_list: list[LetterElement],
        phoneme_list: dfc22_parameters.PhonemeList,
        margin_percentage: float = 0.1,
    ):
        self.letter_canvas = letter_canvas
        self.letter_element_list = letter_element_list
        self._phoneme_list = phoneme_list
        self._image: typing.Optional[Image.Image] = None
        self._margin_percentage = margin_percentage

    def __repr__(self):
        return (
            f"{type(self).__name__}(letter_canvas={self.letter_canvas}, "
            f"letter_element_list={self.letter_element_list}, "
            f"phoneme_list={self.phoneme_list})"
        )

    def _paint(self):
        for letter in self.letter_element_list:
            letter.draw_on(self.letter_canvas)
        # Image.Open(surface.to_png_bytes()) doesn't work!
        # Therefore the workaround by saving the data to a
        # tmp file.
        tmp_name = ".tmp_letter.png"
        self.letter_canvas.surface.write_to_png(tmp_name)
        base_image = Image.open(tmp_name)
        margin_size = int(max(base_image.size) * self._margin_percentage)
        margin_added = margin_size * 2
        new_image = Image.new(
            base_image.mode,
            tuple(size + margin_added for size in base_image.size),
            color='white',
        )
        new_image.paste(base_image, (margin_size, margin_size))
        self._image = new_image
        os.remove(tmp_name)

    @property
    def margin_percentage(self) -> float:
        return self._margin_percentage

    @property
    def image(self) -> Image.Image:
        if self._image is None:
            self._paint()
            return self.image
        return self._image

    @property
    def phoneme_list(self) -> dfc22_parameters.PhonemeList:
        return self._phoneme_list
