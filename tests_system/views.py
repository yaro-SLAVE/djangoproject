from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from tests_system.serializers import *
from django.contrib.auth.models import User

class AuthorizationAPIView(APIView):

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            refresh = RefreshToken.for_user(user) # Создание Refesh и Access

            refresh.payload.update({    # Полезная информация в самом токене

                'user_id': user.id,

                'username': user.username

            })

            return Response({

                'refresh': str(refresh),

                'jwt': str(refresh.access_token), # Отправка на клиент

            })

