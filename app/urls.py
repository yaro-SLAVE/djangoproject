"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from tests_system.api import *
from django.contrib.auth.models import User


router = DefaultRouter()
router.register("users", UserViewset, basename="users")
router.register("profiles", ProfileViewset, basename="profiles")
router.register("roles", RoleViewset, basename="roles")
router.register("groups", GroupViewset, basename="groups")
router.register("topictypes", TopicTypeViewset, basename="topictypes")
router.register("tasks", TaskViewset, basename="tasks")
router.register("tests", TestViewset, basename="tests")
router.register("answeredtasks", AnsweredTaskViewset, basename="answeredtasks")
router.register("finishedtests", FinishedTestViewset, basename="finishedtests")
router.register("finishedtestansweredtasks", FinishedTestAnsweredTaskViewset, basename="finishedtestansweredtasks")
router.register("testtasks", TestTaskViewset, basename="testtasks")
router.register("images", ImageViewset, basename = "images")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls))
]
