from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    image = models.ImageField("Изображение", upload_to="images")

class Group(models.Model):
    group_name = models.TextField("Название группы")

    def __str__(self) -> str:
        return self.group_name

class Role(models.Model):
    role = models.TextField("Название роли")
    description = models.TextField("Описание роли")

    def __str__(self) -> str:
        return self.role

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    total_scores = models.IntegerField("Общее количество баллов", null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    profile_logo = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)

class TopicType(models.Model):
    topic_type_name = models.TextField("Название темы")
    description = models.TextField("Описание роли")

    def __str__(self) -> str:
        return self.topic_type_name
    
class TaskAnswersType(models.Model):
    type_name = models.TextField("Тип ответов")
    description = models.TextField("Описание типа")

    def __str__(self) -> str:
        return self.type_name

class Task(models.Model):
    task_statement = models.TextField("Условие задания")
    topic_type = models.ForeignKey(TopicType, on_delete=models.CASCADE)
    answers_type = models.ForeignKey(TaskAnswersType, on_delete=models.CASCADE)
    task_body = models.JSONField("Тело теста")
    correct_answer = models.IntegerField("Верный ответ")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Test(models.Model):
    name = models.TextField("Название теста")
    topic_type = models.ForeignKey(TopicType, on_delete=models.CASCADE)

class TestTask(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class AnsweredTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    selected_answer = models.IntegerField("Выбранный ответ")

class FinishedTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_of_passage = models.TimeField("Время выполнения")
    test_scores = models.IntegerField("Баллы за ответы")
    bonus_scores = models.IntegerField("Бонусные баллы")
    total_scores = models.IntegerField("Итоговые баллы")

class FinishedTestAnsweredTask(models.Model):
    finished_test = models.ForeignKey(FinishedTest, on_delete=models.CASCADE)
    answered_task = models.ForeignKey(AnsweredTask, on_delete=models.CASCADE)

class TaskImage(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)