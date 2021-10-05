from django.db import models


class Point(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    point_name = models.CharField(max_length=50, default='POINT NAME')


class UserData(models.Model):
    name = models.CharField(max_length=50, default='A A')
    email = models.CharField(max_length=50, default='A@A.com')
    coords = models.OneToOneField(Point, related_name='user_data', on_delete=models.CASCADE)


class User(models.Model):
    user_data = models.OneToOneField(UserData, related_name='user', on_delete=models.CASCADE)
