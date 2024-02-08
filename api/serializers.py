from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from .models import Scheduler, CustomUser, HolidayRequest

class SchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler
        fields = '__all__'

class CreateScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'second_name', 'birth_date', 'mobile_number', 'age', 'employment_start_date', 'employment_end_date', 'role', 'education']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            second_name=validated_data.get('second_name', ''),
            last_name=validated_data.get('last_name', ''),
            birth_date=validated_data.get('birth_date', None),
            mobile_number=validated_data.get('mobile_number', ''),
            age=validated_data.get('age', None),
            employment_start_date=validated_data.get('employment_start_date', None),
            employment_end_date=validated_data.get('employment_end_date', None),
            role=validated_data.get('role', ''),
            education=validated_data.get('education', '')
        )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class CustomUserDataSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

class HolidayRequestSerializer(serializers.Serializer):
    user = CustomUserDataSerializer()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    difference_in_days = serializers.IntegerField()
    selected_holiday_type = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['created_at'] = instance.created_at.strftime("%Y-%m-%d | %H:%M:%S")

        return representation

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance = CustomUser.objects.get(email=user_data.get('email', ''))

        holiday_request = HolidayRequest.objects.create(user=user_instance, **validated_data)
        return holiday_request