from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Scheduler
from .serializers import SchedulerSerializer, CreateScheduleSerializer, UserSerializer, RegisterSerializer
from knox.models import AuthToken
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view

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
            # Utwórz nowy obiekt Scheduler
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class AllDatesView(APIView):
    def get(self, request, format=None):
        # Pobierz wszystkie obiekty z modelu Scheduler
        all_dates = Scheduler.objects.all()
        serializer = SchedulerSerializer(all_dates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClearScheduleView(APIView):
    def delete(self, request, format=None):
        # Usunięcie wszystkich obiektów z modelu Scheduler
        Scheduler.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #
    #     return Response({
    #         'user': UserSerializer(user, context=self.get_serializer_context()).data,
    #         'token': AuthToken.objects.create(user)[1]
    #     })

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = {
            'email': serializer.validated_data['email'],
            'password': serializer.validated_data['password'],
            'first_name': request.data.get('first_name', ''),
            'last_name': request.data.get('last_name', '')
        }

        # user = serializer.save()

        user = serializer.create(validated_data)

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })