from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    group_name = models.TextField("Название группы")

class Role(models.Model):
    role = models.TextField("Название роли")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    total_scores = models.IntegerField("Общее количество баллов")
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

class TopicType(models.Model):
    topic_type_name = models.TextField("Название темы")

class Task(models.Model):
    topic_type = models.ForeignKey(TopicType, on_delete=models.CASCADE)
    task_body = models.JSONField("Тело теста")

class Test(models.Model):
    topic_type = models.ForeignKey(TopicType, on_delete=models.CASCADE)

class TestTask(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class AnsweredTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    selected_answer = models.IntegerField("Выбранный ответ")
    correct_answer = models.IntegerField("Верный ответ")

class FinishedTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time_of_passage = models.TimeField("Время выполнения")
    test_scores = models.IntegerField("Баллы за ответы")
    bonus_scores = models.IntegerField("Бонусные баллы")
    total_scores = models.IntegerField("Итоговые баллы")

class FinishedTestAnsweredTask(models.Model):
    finished_test = models.ForeignKey(FinishedTest, on_delete=models.CASCADE)
    answered_task = models.ForeignKey(AnsweredTask, on_delete=models.CASCADE)