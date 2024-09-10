from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from students.models import Student, Group
from students.serializers import StudentSerializer, GroupSerializer

class StudentsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class GroupsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
