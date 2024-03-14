import uuid
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth import get_user_model
from .models import Scheduler, CustomUser, HolidayRequest, HolidayType, Notification, HolidayPlan

class SchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler
        fields = '__all__'


class HolidayPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidayPlan
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
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'second_name', 'birth_date', 'mobile_number', 'age', 'employment_start_date', 'employment_end_date', 'role', 'education', 'user_residence_data', 'correspondence_address', 'tax_office', 'annual_settlement_address', 'nfz_branch', 'id_data', 'id_given_by', 'id_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            second_name=validated_data.get('second_name', ''),
            last_name=validated_data.get('last_name', ''),
            birth_date=validated_data.get('birth_date', ''),
            mobile_number=validated_data.get('mobile_number', ''),
            age=validated_data.get('age', ''),
            employment_start_date=validated_data.get('employment_start_date', ''),
            employment_end_date=validated_data.get('employment_end_date', ''),
            role=validated_data.get('role', ''),
            education=validated_data.get('education', ''),
            user_residence_data=validated_data.get('user_residence_data', ''),
            correspondence_address=validated_data.get('correspondence_address', ''),
            tax_office=validated_data.get('tax_office', ''),
            annual_settlement_address=validated_data.get('annual_settlement_address', ''),
            nfz_branch=validated_data.get('nfz_branch', ''),
            id_data=validated_data.get('id_data', ''),
            id_given_by=validated_data.get('id_given_by', ''),
            id_date=validated_data.get('id_date', ''),
            city=validated_data.get('city', ''),
            postal_code=validated_data.get('postal_code', ''),
            post=validated_data.get('post', ''),
            municipal_commune=validated_data.get('municipal_commune', ''),
            voivodeship=validated_data.get('voivodeship', ''),
            country=validated_data.get('country', ''),
            street=validated_data.get('street', ''),
            house_number=validated_data.get('house_number', ''),
            flat_number=validated_data.get('flat_number', '')
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
    id = serializers.UUIDField(read_only=True)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    difference_in_days = serializers.IntegerField()
    selected_holiday_type = serializers.CharField()
    message = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    approved = serializers.BooleanField(default=False)
    color_hex = serializers.CharField(max_length=7, allow_blank=True, allow_null=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime("%Y-%m-%d | %H:%M:%S")
        representation['id'] = str(instance.id)
        return representation

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance = CustomUser.objects.get(email=user_data.get('email', ''))
        holiday_request = HolidayRequest.objects.create(user=user_instance, **validated_data)
        return holiday_request




class HolidayTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidayType
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'