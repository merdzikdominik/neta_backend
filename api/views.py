from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Scheduler
from .serializers import SchedulerSerializer, CreateScheduleSerializer
from rest_framework.permissions import IsAuthenticated

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
