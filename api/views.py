from django.shortcuts import render
from rest_framework import generics, status
from .models import Scheduler
from .serializers import SchedulerSerializer, CreateScheduleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class SchedulerView(generics.ListAPIView):
    queryset = Scheduler.objects.all()
    serializer_class = SchedulerSerializer


class CreateScheduleView(APIView):
    serializer_class = CreateScheduleSerializer

    def post(self, request, format=None):
        # Pobierz host z sesji lub utwórz nową sesję
        host = self.request.session.session_key

        if not host:
            self.request.session.create()
            host = self.request.session.session_key

        # Kopiuj dane żądania i dodaj pole 'host'
        mutable_data = request.data.copy()
        mutable_data['host'] = host

        serializer = self.serializer_class(data=mutable_data)

        if serializer.is_valid():
            # Utwórz nowy obiekt Scheduler
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
