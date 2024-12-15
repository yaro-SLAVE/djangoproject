from django.contrib import admin

from tests_system.models import *
from django.contrib.auth.models import User

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "group", "role", "total_scores"]
    

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["id", "group_name"]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "role"]

@admin.register(TopicType)
class TopicTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "topic_type_name"]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "topic_type", "task_body"]

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ["id", "topic_type"]

@admin.register(TestTask)
class TestAdmin(admin.ModelAdmin):
    list_display = ["id", "task", "test"]

@admin.register(TaskAnswersType)
class TaskAnswersTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "type_name", "description"] 