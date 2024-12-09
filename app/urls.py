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

from django.conf.urls.static import static
from django.conf import settings



router = DefaultRouter()
router.register("user", UserViewset, basename="user")
router.register("profile", ProfileViewset, basename="profile")
router.register("role", RoleViewset, basename="role")
router.register("group", GroupViewset, basename="group")
router.register("topic_type", TopicTypeViewset, basename="topic_type")
router.register("task", TaskViewset, basename="task")
router.register("test", TestViewset, basename="test")
router.register("answered_task", AnsweredTaskViewset, basename="answered_task")
router.register("finished_test", FinishedTestViewset, basename="finished_test")
router.register("finished_test_answered_task", FinishedTestAnsweredTaskViewset, basename="finished_test_answered_task")
router.register("test_task", TestTaskViewset, basename="test_task")
router.register("image", ImageViewset, basename = "image")
router.register("task_answers_type", TaskAnswersTypeViewset, basename = "task_answer_type")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', jwt_views.TokenObtainPairView.as_view()),
    path('api/auth/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('api/auth/logout/', jwt_views.TokenBlacklistView.as_view()),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
