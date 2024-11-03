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
from tests_system import views

from rest_framework_simplejwt import views as jwt_views


router = DefaultRouter()
router.register("users", UserViewset, basename="users")
router.register("profiles", ProfileViewset, basename="profiles")
router.register("roles", RoleViewset, basename="roles")
router.register("groups", GroupViewset, basename="groups")
router.register("topic_types", TopicTypeViewset, basename="topic_types")
router.register("tasks", TaskViewset, basename="tasks")
router.register("tests", TestViewset, basename="tests")
router.register("answered_tasks", AnsweredTaskViewset, basename="answered_tasks")
router.register("finished_tests", FinishedTestViewset, basename="finished_tests")
router.register("finished_test_answered_tasks", FinishedTestAnsweredTaskViewset, basename="finished_test_answered_tasks")
router.register("test_tasks", TestTaskViewset, basename="test_tasks")
router.register("images", ImageViewset, basename = "images")
router.register("task_images", TaskImageViewset, basename = "task_images")
router.register("refresh_tokens", RefreshTokenViewset, basename = "refresh_tokens")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("api/", include(router.urls)),
]
