from math import sqrt

from django.http import JsonResponse

from points.models import Point
from points.serializers import PointSerializer


def get_all_points():
    points = Point.objects.all()
    return PointSerializer(points, many=True)


def get_points_by_name(name):
    points = Point.objects.all()
    response_data = []
    for point in points:
        if point.point_name == name:
            response_data.append(point)
    return PointSerializer(response_data, many=True)


def get_point_distance_to_zero(point):
    return get_coords_distance_to_zero(point.x, point.y)

def get_distance_between_points(point1, point2):
    return get_distance_between_coords(point1.x, point1.y, point2.x, point2.y)


def get_coords_distance_to_zero(x, y):
    return get_distance_between_coords(x, y, 0, 0)


def get_distance_between_coords(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_closest_point(point):
    result = None
    points = Point.objects.all()
    if len(points.all()) == 0:
        return 0, None
    is_first = True
    min_dist = 0
    for other_point in points:
        dist = get_distance_between_points(point, other_point)
        if dist < min_dist or is_first:
            is_first = False
            min_dist = dist
            result = other_point
    return min_dist, result


def process_request(request_data):
    serializer = PointSerializer(data=request_data)
    if not serializer.is_valid():
        return False, JsonResponse(serializer.errors, status=400)
    point = serializer.validated_data
    status, result = process_coords(point.get('x'), point.get('y'))
    if not status:
        return status, result
    status, result = process_name(point.get('point_name'))
    if not status:
        return status, result
    distance = get_coords_distance_to_zero(point.get('x'), point.get('y'))
    Point.objects.create(**serializer.data)
    return True, distance


def process_name(name):
    if len(name) < 1:
        return False, JsonResponse(
            {"error": "point_name should contain at least 1 character"},
            status=422)
    else:
        return True, None


def process_coords(x, y):
    if abs(x) > 1000 or abs(y) > 1000:
        return False, JsonResponse(
            {"error": "coords absolute values should be less than 1000"},
            status=422)
    else:
        return True, None
