from django.test import TestCase
from points.models import Point
from points.services import get_coords_distance_to_zero, get_point_distance_to_zero, \
    process_name, get_distance_between_points, get_distance_between_coords, process_coords


class UnitsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_test_point = Point(point_name='a', x=8, y=-6)
        cls.second_test_point = Point(point_name='b', x=-3, y=-4)
        cls.third_test_point = Point(point_name='c', x=1, y=0)

    def test_coords_distance_to_zero(self):
        self.assertEqual(get_coords_distance_to_zero(3, 4), 5)
        self.assertEqual(get_coords_distance_to_zero(0, 1), 1)

    def test_point_distance_to_zero(self):
        self.assertEqual(get_point_distance_to_zero(self.first_test_point), 10)
        self.assertEqual(get_point_distance_to_zero(self.second_test_point), 5)
        self.assertEqual(get_point_distance_to_zero(self.third_test_point), 1)

    def test_distance_between_coords(self):
        self.assertLess(abs(get_distance_between_coords(0, 0, 0, 0) ** 2 - 0), 1e-6)
        self.assertLess(abs(get_distance_between_coords(13, -5, 22, 7) ** 2 - 225), 1e-6)
        self.assertLess(abs(get_distance_between_coords(2, 2, 0, 0) ** 2 - 8), 1e-6)

    def test_distance_between_same_points(self):
        self.assertEqual(get_distance_between_points(self.first_test_point, self.first_test_point), 0)
        self.assertEqual(get_distance_between_points(self.second_test_point, self.second_test_point), 0)
        self.assertEqual(get_distance_between_points(self.third_test_point, self.third_test_point), 0)

    def test_distance_between_points(self):
        self.assertLess(abs(get_distance_between_points(
            self.first_test_point, self.second_test_point) ** 2 - 125), 1e-6)
        self.assertLess(abs(get_distance_between_points(
            self.second_test_point, self.third_test_point) ** 2 - 32), 1e-6)
        self.assertLess(abs(get_distance_between_points(
            self.third_test_point, self.first_test_point) ** 2 - 85), 1e-6)

    def test_process_name(self):
        status, result = process_name('a')
        self.assertTrue(status)
        self.assertIsNone(result)

    def test_process_bad_name(self):
        status, result = process_name('')
        self.assertFalse(status)
        self.assertIsNotNone(result)

    def test_process_coords(self):
        status, result = process_coords(100, -208)
        self.assertTrue(status)
        self.assertIsNone(result)

    def test_process_bad_coords(self):
        status, result = process_coords(1001, 500)
        self.assertFalse(status)
        self.assertIsNotNone(result)
