from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth import login
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status, generics, permissions
# from rest_framework.permissions import IsAuthenticated
from .models import Scheduler
from .serializers import SchedulerSerializer, CreateScheduleSerializer, UserSerializer, RegisterSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication



class SchedulerView(generics.ListAPIView):
    queryset = Scheduler.objects.all()
    serializer_class = SchedulerSerializer
@method_decorator(csrf_exempt, name='dispatch')
class CreateScheduleView(APIView):
    serializer_class = CreateScheduleSerializer

    def post(self, request, format=None):
        host = request.session.session_key

        if not host:
            request.session.create()
            host = request.session.session_key

        mutable_data = request.data.copy()
        mutable_data['host'] = host

        serializer = self.serializer_class(data=mutable_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class AllDatesView(APIView):
    def get(self, request, format=None):
        all_dates = Scheduler.objects.all()
        serializer = SchedulerSerializer(all_dates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClearScheduleView(APIView):
    def delete(self, request, format=None):
        Scheduler.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = {
            'email': serializer.validated_data['email'],
            'password': serializer.validated_data['password'],
            'first_name': request.data.get('first_name', ''),
            'second_name': request.data.get('second_name', ''),
            'last_name': request.data.get('last_name', ''),
            'birth_date': request.data.get('birth_date', ''),
            'mobile_number': request.data.get('mobile_number', ''),
            'age': request.data.get('age', ''),
            'employment_start_date': request.data.get('employment_start_date', ''),
            'employment_end_date': request.data.get('employment_end_date', ''),
            'role': request.data.get('role', ''),
            'education': request.data.get('education', '')
        }

        user = serializer.create(validated_data)

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })

# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         user = serializer.validated_data['user']
#
#         login(request, user)
#
#         # return super(LoginAPI, self).post(request, format=None)
#
#         user_data = UserSerializer(user, context=self.get_serializer_context()).data
#         response_data = {
#             'user': user_data,
#             'is_superuser': user.is_superuser,
#             'token': serializer.validated_data['token']
#         }

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        login(request, user)

        # Sprawdź, czy token istnieje, jeśli tak, to go zapisz
        token = AuthToken.objects.create(user)
        if token:
            response_data = {
                'user': UserSerializer(user, context=self).data,
                'is_superuser': user.is_superuser,
                'token': token[1],
            }
        else:
            response_data = {
                'user': UserSerializer(user, context=self).data,
                'is_superuser': user.is_superuser,
            }

        return Response(response_data)

class UserInfoAPI(APIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)