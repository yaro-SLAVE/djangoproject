from rest_framework import serializers

from tests_system.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset = Group.objects.all(), read_only = False)
    role = serializers.PrimaryKeyRelatedField(queryset = Role.objects.all(), read_only = False)
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only = False)
    image = serializers.PrimaryKeyRelatedField(queryset = Image.objects.all(), read_only = False)

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user.id

            return super().create(validated_data)

    class Meta:
        model = Profile
        fields = "__all__"

class TopicTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicType
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    topic_type = serializers.PrimaryKeyRelatedField(queryset = TopicType.objects.all(), read_only = False)
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only = False)

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user.id

            return super().create(validated_data)

    class Meta:
        model = Task
        fields = "__all__"

class TestSerializer(serializers.ModelSerializer):
    topic_type = serializers.PrimaryKeyRelatedField(queryset = TopicType.objects.all(), read_only = False)

    class Meta:
        model = Test
        fields = "__all__"

class TestTaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset = Task.objects.all(), read_only = False)
    test = serializers.PrimaryKeyRelatedField(queryset = Test.objects.all(), read_only = False)

    class Meta:
        model = TestTask
        fields = "__all__"

class AnsweredTaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset = Task.objects.all(), read_only = False)

    class Meta:
        model = AnsweredTask
        fields = "__all__"

class FinishedTestSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(queryset = Test.objects.all(), read_only = False)
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only = False)

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user.id

            return super().create(validated_data)

    class Meta:
        model = FinishedTest
        fields = "__all__"

class FinishedTestAnsweredTaskSerializer(serializers.ModelSerializer):
    finished_test = serializers.PrimaryKeyRelatedField(queryset = FinishedTest.objects.all(), read_only = False)
    answered_task = serializers.PrimaryKeyRelatedField(queryset = AnsweredTask.objects.all(), read_only = False)

    class Meta:
        model = FinishedTestAnsweredTask
        fields = "__all__"

class TaskImageSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset = Task.objects.all(), read_only = False)
    image = serializers.PrimaryKeyRelatedField(queryset = Image.objects.all(), read_only = False)

    class Meta:
        model = Image
        fields = "__all__"

class RefreshTokenSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only = False)

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user.id

            return super().create(validated_data)

    class Meta:
        model = RefreshToken
        fields = "__all__"    