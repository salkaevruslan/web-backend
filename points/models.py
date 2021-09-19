from django.db import models


class Point(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    point_name = models.CharField(max_length=50, default='POINT NAME')
