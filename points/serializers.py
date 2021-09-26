from rest_framework import serializers


class PointSerializer(serializers.Serializer):
    x = serializers.FloatField(default=0.0)
    y = serializers.FloatField(default=0.0)
    point_name = serializers.CharField(max_length=50, allow_blank=True)
