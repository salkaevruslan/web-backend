import json

from django.test import TestCase
from django.urls import reverse

from points.models import Point
from points.serializers import PointSerializer


class IntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Point.objects.all().delete()
        cls.first_test_point = Point.objects.create(point_name='a', x=8, y=-6)
        cls.second_test_point = Point.objects.create(point_name='b', x=-3, y=-4)
        cls.third_test_point = Point.objects.create(point_name='c', x=1, y=0)

    def test_get_points_without_name(self):
        response = self.client.get(reverse('points'))
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        serializer = PointSerializer(data=json_data, many=True)
        self.assertTrue(serializer.is_valid())
        points = serializer.validated_data
        self.assertEqual(len(points), 3)
        for point in points:
            self.assertTrue(point.get('point_name') in ['a', 'b', 'c'])
            x = point.get('x')
            y = point.get('y')
            self.assertTrue((x, y) in [(8, -6), (-3, -4), (1, 0)])

    def test_get_points_with_correct_name(self):
        response = self.client.get(reverse('points'), {'point_name': 'a'})
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        serializer = PointSerializer(data=json_data, many=True)
        self.assertTrue(serializer.is_valid())
        points = serializer.validated_data
        self.assertEqual(len(points), 1)
        for point in points:
            self.assertEqual(point.get('point_name'), 'a')
            x = point.get('x')
            y = point.get('y')
            self.assertEqual(x, 8)
            self.assertEqual(y, -6)

    def test_get_points_with_incorrect_name(self):
        response = self.client.get(reverse('points'), {'point_name': 'z'})
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        serializer = PointSerializer(data=json_data, many=True)
        self.assertTrue(serializer.is_valid())
        points = serializer.validated_data
        self.assertEqual(len(points), 0)

    def test_post_correct_data(self):
        response = self.client.post(reverse('points'), {'x': '-4', 'y': '3', 'point_name': 'z'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertLess(abs(json_data.get('distance to zero') ** 2 - 25), 1e-6)
        self.assertEqual(len(Point.objects.all()), 4)

    def test_post_incorrect_name(self):
        response = self.client.post(reverse('points'), {'x': '-4', 'y': '3', 'point_name': ''},
                                    content_type='application/json')
        print(response.content)
        self.assertEqual(response.status_code, 422)

    def test_post_incorrect_coords(self):
        response = self.client.post(reverse('points'), {'x': '1001', 'y': '3', 'point_name': 'asdf'},
                                    content_type='application/json')
        print(response.content)
        self.assertEqual(response.status_code, 422)
