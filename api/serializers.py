from rest_framework import serializers
from .models import Scheduler

class SchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler
        fields = '__all__'

class CreateScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler
        fields = '__all__'

