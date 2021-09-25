from django.urls import path
from .views import PointView

urlpatterns = [
    path('point/', PointView.as_view(), name='points')
]
