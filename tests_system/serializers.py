from rest_framework import serializers
from tests_system.models import *
from django.contrib.auth.models import User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only = True)
    group_id = serializers.PrimaryKeyRelatedField(queryset = Group.objects.all(), source = 'group', write_only = True)
    role = RoleSerializer(read_only = True)
    role_id = serializers.PrimaryKeyRelatedField(queryset = Role.objects.all(), source = 'role', write_only = True)
    user = UserSerializer(read_only = True)
    user_id = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), source = 'user', write_only = True)

    class Meta:
        model = Profile
        fields = "__all__"

class TopicTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicType
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    topic_type = TopicTypeSerializer(read_only = True)
    topic_type_id = serializers.PrimaryKeyRelatedField(queryset = TopicType.objects.all(), source = 'topic_type', write_only = True)

    class Meta:
        model = Task
        fields = "__all__"

class TestSerializer(serializers.ModelSerializer):
    topic_type = TopicTypeSerializer(read_only = True)
    topic_type_id = serializers.PrimaryKeyRelatedField(queryset = TopicType.objects.all(), source = 'topic_type', write_only = True)

    class Meta:
        model = Test
        fields = "__all__"

class TestTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only = True)
    task_id = serializers.PrimaryKeyRelatedField(queryset = Task.objects.all(), source = 'task', write_only = True)
    test = TestSerializer(read_only = True)
    test_id = serializers.PrimaryKeyRelatedField(queryset = Test.objects.all(), source = 'test', write_only = True)

    class Meta:
        model = TestTask
        fields = "__all__"

class AnsweredTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only = True)
    task_id = serializers.PrimaryKeyRelatedField(queryset = Task.objects.all(), source = 'task', write_only = True)

    class Meta:
        model = AnsweredTask
        fields = "__all__"

class FinishedTestSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only = True)
    test_id = serializers.PrimaryKeyRelatedField(queryset = Test.objects.all(), source = 'test', write_only = True)
    profile = ProfileSerializer(read_only = True)
    profile_id = serializers.PrimaryKeyRelatedField(queryset = Profile.objects.all(), source = 'progile', write_only = True)

    class Meta:
        model = FinishedTest
        fields = "__all__"

class FinishedTestAnsweredTaskSerializer(serializers.ModelSerializer):
    finished_test = FinishedTestSerializer(read_only = True)
    finished_test_id = serializers.PrimaryKeyRelatedField(queryset = FinishedTest.objects.all(), source = 'finished_test', write_only = True)
    answered_task = AnsweredTaskSerializer(read_only = True)
    answered_task_id = serializers.PrimaryKeyRelatedField(queryset = AnsweredTask.objects.all(), source = 'answered_task', write_only = True)

    class Meta:
        model = FinishedTestAnsweredTask
        fields = "__all__"

class ImageSerializer(serializers.ModelSerializer):
    topic_type = TopicTypeSerializer(read_only = True)
    topic_type_id = serializers.PrimaryKeyRelatedField(queryset = TopicType.objects.all(), source = 'topic_type', write_only = True)

    class Meta:
        model = Image
        fields = "__all__"