import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from points.models import Point, UserData, User


class PointType(DjangoObjectType):
    class Meta:
        model = Point
        fields = ('id', 'x', 'y', 'point_name')
        filter_fields = ('id', 'point_name')
        interfaces = [relay.Node]


class UserDataType(DjangoObjectType):
    class Meta:
        model = UserData
        fields = ('id', 'coords', 'name', 'email')
        filter_fields = ['id', 'name', 'email']
        interfaces = [relay.Node]


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'user_data')
        filter_fields = ['id']
        interfaces = [relay.Node]


class Query(graphene.ObjectType):
    point = relay.Node.Field(PointType)
    all_points = DjangoFilterConnectionField(PointType)
    user_data = relay.Node.Field(UserDataType)
    all_user_data = DjangoFilterConnectionField(UserDataType)
    user = relay.Node.Field(UserType)
    all_users = DjangoFilterConnectionField(UserType)


schema = graphene.Schema(query=Query)
