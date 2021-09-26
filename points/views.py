from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from points.services import get_all_points, get_points_by_name, process_request


@method_decorator(csrf_exempt, name='dispatch')
class PointView(View):
    def get(self, request):
        name = request.GET.get("point_name")
        if name is None:
            serializer = get_all_points()
        else:
            serializer = get_points_by_name(name)
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request):
        request_data = JSONParser().parse(request)
        status, result = process_request(request_data)
        if status:
            return JsonResponse(
                {"distance to zero": result},
                status=200)
        else:
            return result
