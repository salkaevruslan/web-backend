from django.test import TestCase

from points.models import Point
from points.services import get_all_points, get_points_by_name, get_closest_point, process_request


class IntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Point.objects.all().delete()
        cls.first_test_point = Point.objects.create(point_name='a', x=8, y=-6)
        cls.second_test_point = Point.objects.create(point_name='b', x=-3, y=-4)
        cls.third_test_point = Point.objects.create(point_name='c', x=1, y=0)

    def test_get_all_points_names(self):
        serializer = get_all_points()
        self.assertEqual(len(serializer.data), 3)
        for point in serializer.data:
            name = point.get('point_name')
            self.assertTrue(name in ['a', 'b', 'c'])

    def test_get_all_points_coords(self):
        serializer = get_all_points()
        self.assertEqual(len(serializer.data), 3)
        for point in serializer.data:
            x = point.get('x')
            y = point.get('y')
            self.assertTrue((x, y) in [(8, -6), (-3, -4), (1, 0)])

    def test_get_point_by_name(self):
        serializer = get_points_by_name('a')
        self.assertEqual(len(serializer.data), 1)
        for point in serializer.data:
            x = point.get('x')
            y = point.get('y')
            self.assertEqual(point.get('point_name'), 'a')
            self.assertEqual(x, 8)
            self.assertEqual(y, -6)

    def test_get_point_by_name_wrong_name(self):
        serializer = get_points_by_name('z')
        self.assertEqual(len(serializer.data), 0)

    def test_get_closest_point(self):
        distance, result = get_closest_point(Point(point_name='asd', x=100, y=-55))
        self.assertLess(abs(distance ** 2 - 10865), 1e-6)
        self.assertEqual(result.point_name, 'a')
        self.assertEqual(result.x, 8)
        self.assertEqual(result.y, -6)

    def test_get_closest_point_exists_same(self):
        distance, result = get_closest_point(Point(point_name='asd', x=1, y=0))
        self.assertLess(abs(distance ** 2 - 0), 1e-6)
        self.assertEqual(result.point_name, 'c')
        self.assertEqual(result.x, 1)
        self.assertEqual(result.y, 0)

    def test_adding_points(self):
        status, result = process_request({'x': 3, 'y': 4, 'point_name': 'z'})
        self.assertEqual(result, 5)
        self.assertTrue(status)
        status, result = process_request({'x': 0, 'y': -1, 'point_name': 't'})
        self.assertEqual(result, 1)
        self.assertTrue(status)
        serializer = get_points_by_name('z')
        self.assertEqual(len(serializer.data), 1)
        for point in serializer.data:
            self.assertEqual(point.get('point_name'), 'z')
            self.assertEqual(point.get('x'), 3)
            self.assertEqual(point.get('y'), 4)
        serializer = get_points_by_name('t')
        self.assertEqual(len(serializer.data), 1)
        for point in serializer.data:
            self.assertEqual(point.get('point_name'), 't')
            self.assertEqual(point.get('x'), 0)
            self.assertEqual(point.get('y'), -1)

