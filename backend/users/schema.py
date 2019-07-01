from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

from projects.models import UserProfile


class UserType(DjangoObjectType):
    class Meta:
        model = UserProfile


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return UserProfile.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('User not logged in')
        return UserProfile.objects.get(user=user)