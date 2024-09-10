from django.test import TestCase
from rest_framework.test import APIClient
from students.models import Student, Group
from model_bakery import baker

class StudentsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        grp = baker.make("students.Group")

        student = baker.make("Student", group = grp)

        r = self.client.get('/api/students/')
        data = r.json()
        print(data)

        assert student.name == data[0]['name']
        assert student.id == data[0]['id']
        assert student.group.id == data[0]['group']['id']
        assert len(data) == 1