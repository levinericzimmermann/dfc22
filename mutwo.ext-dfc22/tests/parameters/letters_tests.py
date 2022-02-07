import unittest

import geometer

from mutwo import dfc22_parameters


class PolygonTest(unittest.TestCase):
    def _test_point_tuple(
        self,
        result_point_tuple: tuple[geometer.Point, ...],
        expected_point_tuple: tuple[geometer.Point, ...],
    ):
        for result_point, expected_point in zip(
            result_point_tuple, expected_point_tuple
        ):
            for (
                result_axis,
                expected_axis,
            ) in zip(result_point.array[:2], expected_point.array):
                self.assertAlmostEqual(expected_axis, round(result_axis, 5), places=4)


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
            initial_point_tuple, 90
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


class QuadTest(unittest.TestCase):
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


class PentagonTest(unittest.TestCase):
    def test_angle_proportion_sequence_to_angle_tuple(self):
        self.assertEqual(
            dfc22_parameters.Pentagon._angle_proportion_sequence_to_angle_tuple(
                angle_proportion_sequence=(1, 1, 1, 1, 1)
            ),
            (108, 108, 108, 108, 108),
        )


if __name__ == "__main__":
    unittest.main()
