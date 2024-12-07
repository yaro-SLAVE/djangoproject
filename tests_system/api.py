from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from rest_framework.permissions import BasePermission 

from tests_system.models import *
from tests_system.serializers import *
from django.contrib.auth.models import User

from django.db.models import Avg, Min, Max, Count

from rest_framework.response import Response

from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
import pyotp

from django.core.cache import cache

from django.conf import settings

class UserViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(url_path="auth_info", methods=["GET"], detail = False)
    def get_auth_info(self, request, *args, **kwargs):
        user = request.user
        user_info = {
            "is_auth": user.is_authenticated
        }

        return Response(user_info)

class ProfileViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    @action(url_path="info", methods=["GET"], detail = False,  permission_classes = [IsAuthenticated])
    def get_info(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user = user.id)
        #profile_full_info = Profile.objects.filter(role = profile.role, group = profile.group).select_related()
        user_info = {
            "is_superuser": user.is_superuser,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": profile.role.role,
            "role_description": profile.role.description,
            "email": user.email,
            "total_scores": profile.total_scores
        }

        if (profile.role == 'student'):
            user_info.update({
                "group": profile.group.group_name
            })

        if (profile.profile_logo != None):
            user_info.update({
                "logo": profile.profile_logo.image.url
            })

        return Response(user_info)
    
    @action(url_path="user_id", methods=["GET"], detail = False)
    def get_user_id(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user = user.id)
        user_info = {
            "id": profile.id
        }

        return Response(user_info)
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Profile.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)


class RoleViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Role.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)


class GroupViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Group.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)


class TopicTypeViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = TopicType.objects.all()
    serializer_class = TopicTypeSerializer
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = TopicType.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)

class TaskAnswersTypeViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = TaskAnswersType.objects.all()
    serializer_class = TaskAnswersTypeSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = TaskAnswersType.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)

class TaskViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user = self.request.user.id)
        return qs
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Task.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)

class TestViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Test.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)

class AnsweredTaskViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = AnsweredTask.objects.all()
    serializer_class = AnsweredTaskSerializer
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = AnsweredTask.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)

class TestTaskViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = TestTask.objects.all()
    serializer_class = TestTaskSerializer
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = TestTask.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)

class FinishedTestViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = FinishedTest.objects.all()
    serializer_class = FinishedTestSerializer
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = FinishedTest.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)

class FinishedTestAnsweredTaskViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = FinishedTestAnsweredTask.objects.all()
    serializer_class = FinishedTestAnsweredTaskSerializer
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = FinishedTestAnsweredTask.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)

class ImageViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail = False, methods = ["GET"], url_path = "stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Image.objects.aggregate(
            count = Count("*"),
            avg = Avg("id"),
            min = Min("id"),
            max = Max("id")
        )

        serializer = self.StatsSerializer(isinstance = stats)
        return Response(serializer.data)
    
class TaskImageViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = TaskImage.objects.all()
    serializer_class = TaskImageSerializer