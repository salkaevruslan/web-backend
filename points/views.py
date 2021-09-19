from math import sqrt

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from points.models import Point
from points.serializers import PointSerializer


@method_decorator(csrf_exempt, name='dispatch')
class PointView(View):
    def get(self, request):
        points = Point.objects.all()
        name = request.GET.get("point_name")

        response_data = []
        for point in points:
            if point.point_name == name:
                response_data.append(point)

        serializer = PointSerializer(response_data, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        request_data = JSONParser().parse(request)
        serializer = PointSerializer(data=request_data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        point = serializer.validated_data
        if abs(point.get('x')) > 1000 or abs(point.get('y')) > 1000:
            return JsonResponse(
                {"error": "coords absolute values should be less than 1000"},
                status=422)
        if len(point.get('point_name')) < 1:
            return JsonResponse(
                {"error": "point_name should contain at least 1 character"},
                status=422)
        distance = sqrt(point.get('x') ** 2 + point.get('y') ** 2)
        Point.objects.create(**serializer.data)

        return JsonResponse(
            {"distance to zero": distance},
            status=200)
