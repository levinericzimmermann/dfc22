import unittest

import geometer

from mutwo import dfc22_parameters


class PolygonTest(unittest.TestCase):
    def _test_point(self, result_point: geometer.Point, expected_point: geometer.Point):
        for (result_axis, expected_axis,) in zip(
            result_point.normalized_array[:2], expected_point.normalized_array[:2]
        ):
            self.assertAlmostEqual(expected_axis, round(result_axis, 5), places=4)

    def _test_point_tuple(
        self,
        result_point_tuple: tuple[geometer.Point, ...],
        expected_point_tuple: tuple[geometer.Point, ...],
    ):
        for result_point, expected_point in zip(
            result_point_tuple, expected_point_tuple
        ):
            self._test_point(result_point, expected_point)


class SpecifiedPolygonTest(PolygonTest):
    def test_next_point(self):
        """Assert with various degrees that the next_point function works"""

        self._test_point(
            dfc22_parameters.Polygon._find_next_point(
                geometer.Segment(geometer.Point(0, 0), geometer.Point(-1, 0)), 45, 2
            ),
            geometer.Point(0.41421356237309515, 1.4142135623730951),
        )
        self._test_point(
            dfc22_parameters.Polygon._find_next_point(
                geometer.Segment(geometer.Point(0, 0), geometer.Point(-1, 0)), 90, 2
            ),
            geometer.Point(-1, 2),
        )
        self._test_point(
            dfc22_parameters.Polygon._find_next_point(
                geometer.Segment(geometer.Point(0, 0), geometer.Point(-1, 0)), 180, 2
            ),
            geometer.Point(-3, 0),
        )
        self._test_point(
            dfc22_parameters.Polygon._find_next_point(
                geometer.Segment(geometer.Point(0, 0), geometer.Point(-1, 0)), 360, 3
            ),
            geometer.Point(2, 0),
        )


class TriangleTest(PolygonTest):
    def test_angle_proportion_sequence_to_angle_tuple(self):
        self.assertEqual(
            dfc22_parameters.Triangle._angle_proportion_sequence_to_angle_tuple(
                angle_proportion_sequence=(1, 1, 1)
            ),
            (60, 60, 60),
        )
        self.assertEqual(
            dfc22_parameters.Triangle._angle_proportion_sequence_to_angle_tuple(
                angle_proportion_sequence=(2, 1, 1)
            ),
            (90, 45, 45),
        )

    def test_angles_and_lenghts_to_point_tuple(self):
        result_point_tuple = (
            dfc22_parameters.Triangle._angles_and_lenghts_to_point_tuple(
                (60, 60, 60), (1,)
            )
        )
        expected_point_tuple = (
            geometer.Point(0, 0),
            geometer.Point(-1, 0),
            geometer.Point(-0.5, 0.86603),
        )
        self._test_point_tuple(result_point_tuple, expected_point_tuple)

    def test_rotate_point_tuple(self):
        initial_point_tuple = (
            geometer.Point(0.5, -0.28868),
            geometer.Point(-0.5, -0.28868),
            geometer.Point(0, 0.57735),
        )
        expected_point_tuple = (
            geometer.Point(-0.5, 0.28868),
            geometer.Point(0.5, 0.28868),
            geometer.Point(0, -0.57735),
        )
        result_point_tuple = dfc22_parameters.Polygon._rotate_point_tuple(
            initial_point_tuple, 180
        )
        self._test_point_tuple(result_point_tuple, expected_point_tuple)

    def test_from_angles_and_length(self):
        polygon = dfc22_parameters.Triangle.from_angles_and_lengths(
            angle_proportion_sequence=(60, 60, 60), length_proportion_sequence=(1,)
        )

        expected_point_tuple = (
            geometer.Point(0.5, -0.28868),
            geometer.Point(-0.5, -0.28868),
            geometer.Point(0, 0.57735),
        )
        self._test_point_tuple(tuple(polygon.vertices), expected_point_tuple)

    def test_draw_on(self):
        triangle = dfc22_parameters.Triangle.from_angles_and_lengths(
            angle_proportion_sequence=(1, 1, 1), length_proportion_sequence=(1,)
        )
        letter_canvas = dfc22_parameters.LetterCanvas(800, 800)
        triangle.draw_on(letter_canvas)
        letter_canvas.surface.write_to_png("tests/parameters/triangle_draw_test.png")


class QuadTest(PolygonTest):
    def test_angle_proportion_sequence_to_angle_tuple(self):
        self.assertEqual(
            dfc22_parameters.Quad._angle_proportion_sequence_to_angle_tuple(
                angle_proportion_sequence=(1, 1, 1, 1)
            ),
            (90, 90, 90, 90),
        )
        self.assertEqual(
            dfc22_parameters.Quad._angle_proportion_sequence_to_angle_tuple(
                angle_proportion_sequence=(2, 1, 3, 4)
            ),
            (72, 36, 108, 144),
        )

    def test_angles_and_lenghts_to_point_tuple(self):
        # with equal angle and two different side lengths
        result_point_tuple = dfc22_parameters.Quad._angles_and_lenghts_to_point_tuple(
            (90, 90, 90, 90), (1, 2)
        )
        expected_point_tuple = (
            geometer.Point(0, 0),
            geometer.Point(-1, 0),
            geometer.Point(-1, 2),
            geometer.Point(0, 2),
        )
        self._test_point_tuple(result_point_tuple, expected_point_tuple)

    def test_get_centroid(self):
        quad = dfc22_parameters.Quad.from_angles_and_lengths(
            angle_proportion_sequence=(1, 1, 1, 1),
            length_proportion_sequence=(1, 1),
            max_length=1,
        )
        letter_canvas = dfc22_parameters.LetterCanvas(100, 100)
        self._test_point(quad.get_centroid(letter_canvas), geometer.Point(50, 50))

    def test_get_adjusted_point_tuple(self):
        quad = dfc22_parameters.Quad.from_angles_and_lengths(
            angle_proportion_sequence=(1, 1, 1, 1),
            length_proportion_sequence=(1, 1),
            max_length=1,
        )
        letter_canvas = dfc22_parameters.LetterCanvas(100, 100)
        result_point_tuple = quad._get_adjusted_point_tuple(letter_canvas)
        expected_point_tuple = (
            geometer.Point(100, 0),
            geometer.Point(0, 0),
            geometer.Point(0, 100),
            geometer.Point(100, 100),
        )
        self._test_point_tuple(result_point_tuple, expected_point_tuple)


class PentagonTest(PolygonTest):
    def test_angle_proportion_sequence_to_angle_tuple(self):
        self.assertEqual(
            dfc22_parameters.Pentagon._angle_proportion_sequence_to_angle_tuple(
                angle_proportion_sequence=(1, 1, 1, 1, 1)
            ),
            (108, 108, 108, 108, 108),
        )


if __name__ == "__main__":
    unittest.main()
