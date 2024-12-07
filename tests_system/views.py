from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from tests_system.serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status

class AuthorizationAPIView(APIView):

    def post(self, request):

        data = request.data

        username = data.get('username', None)

        password = data.get('password', None)

        if username is None or password is None:

            return Response({'error': 'Нужен и логин, и пароль'},

                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:

            return Response({'error': 'Неверные данные'},

                            status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        refresh.payload.update({

            'user_id': user.id,

            'username': user.username

        })

        Response.set_cookie("jwt", value=refresh.access_token, max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite=None)
        Response.set_cookie("refresh", value=refresh, max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite=None)

        return Response({

            'refresh': str(refresh),

            'access': str(refresh.access_token),

        })

