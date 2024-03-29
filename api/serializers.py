import uuid
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth import get_user_model
from .models import Scheduler, CustomUser, HolidayRequest, HolidayType, Notification, HolidayPlan, DataChangeRequest

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
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'password',
                  'second_name',
                  'birth_date',
                  'age',
                  'employment_start_date',
                  'employment_end_date',
                  'role',
                  'education',
                  # 'user_residence_data',
                  'correspondence_address',
                  'tax_office',
                  'annual_settlement_address',
                  'nfz_branch',
                  'id_data',
                  'id_given_by',
                  'id_date',
                  'mobile_number_permanent_residence',
                  'city_permanent_residence',
                  'postal_code_permanent_residence',
                  'post_permanent_residence',
                  'municipal_commune_permanent_residence',
                  'voivodeship_permanent_residence',
                  'country_permanent_residence',
                  'street_permanent_residence',
                  'house_number_permanent_residence',
                  'flat_number_permanent_residence',
                  'mobile_number_second_residence',
                  'city_second_residence',
                  'postal_code_second_residence',
                  'post_second_residence',
                  'municipal_commune_second_residence',
                  'voivodeship_second_residence',
                  'country_second_residence',
                  'street_second_residence',
                  'house_number_second_residence',
                  'flat_number_second_residence',
                  'mobile_number_correspondence',
                  'city_correspondence',
                  'postal_code_correspondence',
                  'post_correspondence',
                  'municipal_commune_correspondence',
                  'voivodeship_correspondence',
                  'country_correspondence',
                  'street_correspondence',
                  'house_number_correspondence',
                  'flat_number_correspondence'
                  ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            second_name=validated_data.get('second_name', ''),
            last_name=validated_data.get('last_name', ''),
            birth_date=validated_data.get('birth_date', ''),
            age=validated_data.get('age', ''),
            employment_start_date=validated_data.get('employment_start_date', ''),
            employment_end_date=validated_data.get('employment_end_date', ''),
            role=validated_data.get('role', ''),
            education=validated_data.get('education', ''),
            correspondence_address=validated_data.get('correspondence_address', ''),
            tax_office=validated_data.get('tax_office', ''),
            annual_settlement_address=validated_data.get('annual_settlement_address', ''),
            nfz_branch=validated_data.get('nfz_branch', ''),
            id_data=validated_data.get('id_data', ''),
            id_given_by=validated_data.get('id_given_by', ''),
            id_date=validated_data.get('id_date', ''),
            mobile_number_permanent_residence=validated_data.get('mobile_number_permanent_residence', ''),
            city_permanent_residence=validated_data.get('city_permanent_residence', ''),
            postal_code_permanent_residence=validated_data.get('postal_code_permanent_residence', ''),
            post_permanent_residence=validated_data.get('post_permanent_residence', ''),
            municipal_commune_permanent_residence=validated_data.get('municipal_commune_permanent_residence', ''),
            voivodeship_permanent_residence=validated_data.get('voivodeship_permanent_residence', ''),
            country_permanent_residence=validated_data.get('country_permanent_residence', ''),
            street_permanent_residence=validated_data.get('street_permanent_residence', ''),
            house_number_permanent_residence=validated_data.get('house_number_permanent_residence', ''),
            flat_number_permanent_residence=validated_data.get('flat_number_permanent_residence', ''),
            mobile_number_second_residence=validated_data.get('mobile_number_second_residence', ''),
            city_second_residence=validated_data.get('city_second_residence', ''),
            postal_code_second_residence=validated_data.get('postal_code_second_residence', ''),
            post_second_residence=validated_data.get('post_second_residence', ''),
            municipal_commune_second_residence=validated_data.get('municipal_commune_second_residence', ''),
            voivodeship_second_residence=validated_data.get('voivodeship_second_residence', ''),
            country_second_residence=validated_data.get('country_second_residence', ''),
            street_second_residence=validated_data.get('street_second_residence', ''),
            house_number_second_residence=validated_data.get('house_number_second_residence', ''),
            flat_number_second_residence=validated_data.get('flat_number_second_residence', ''),
            mobile_number_correspondence=validated_data.get('mobile_number_correspondence', ''),
            city_correspondence=validated_data.get('city_correspondence', ''),
            postal_code_correspondence=validated_data.get('postal_code_correspondence', ''),
            post_correspondence=validated_data.get('post_correspondence', ''),
            municipal_commune_correspondence=validated_data.get('municipal_commune_correspondence', ''),
            voivodeship_correspondence=validated_data.get('voivodeship_correspondence', ''),
            country_correspondence=validated_data.get('country_correspondence', ''),
            street_correspondence=validated_data.get('street_correspondence', ''),
            house_number_correspondence=validated_data.get('house_number_correspondence', ''),
            flat_number_correspondence=validated_data.get('flat_number_correspondence', '')
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


class DataChangeRequestSerializer(serializers.Serializer):
    user = CustomUserDataSerializer()
    id = serializers.UUIDField(read_only=True)
    surname = serializers.CharField(required=False, allow_blank=True, default='')
    city_permanent_residence = serializers.CharField(required=False, allow_blank=True, default='')
    postal_code_permanent_residence = serializers.CharField(required=False, allow_blank=True, default='')
    post_permanent_residence = serializers.CharField(required=False, allow_blank=True, default='')
    municipal_commune_permanent_residence = serializers.CharField(required=False, allow_blank=True, default='')
    voivodeship_permanent_residence = serializers.CharField(required=False, allow_blank=True, default='')
    country_permanent_residence = serializers.CharField(required=False, allow_blank=True, default='')
    street_permanent_residence = serializers.CharField(required=False, allow_blank=True, default='')
    house_number_permanent_residence = serializers.CharField(required=False, allow_blank=True, default='')
    flat_number_permanent_residence = serializers.CharField(required=False, allow_blank=True, default='')
    mobile_number_permanent_residence = serializers.CharField(required=False, allow_blank=True, default='')
    city_second_residence = serializers.CharField(required=False, allow_blank=True, default='')
    postal_code_second_residence = serializers.CharField(required=False, allow_blank=True, default='')
    post_second_residence = serializers.CharField(required=False, allow_blank=True, default='')
    municipal_commune_second_residence = serializers.CharField(required=False, allow_blank=True, default='')
    voivodeship_second_residence = serializers.CharField(required=False, allow_blank=True, default='')
    country_second_residence = serializers.CharField(required=False, allow_blank=True, default='')
    street_second_residence = serializers.CharField(required=False, allow_blank=True, default='')
    house_number_second_residence = serializers.CharField(required=False, allow_blank=True, default='')
    flat_number_second_residence = serializers.CharField(required=False, allow_blank=True, default='')
    mobile_number_second_residence = serializers.CharField(required=False, allow_blank=True, default='')
    city_correspondence_residence = serializers.CharField(required=False, allow_blank=True, default='')
    postal_code_correspondence_residence = serializers.CharField(required=False, allow_blank=True, default='')
    post_correspondence_residence = serializers.CharField(required=False, allow_blank=True, default='')
    municipal_commune_correspondence_residence = serializers.CharField(required=False, allow_blank=True, default='')
    voivodeship_correspondence_residence = serializers.CharField(required=False, allow_blank=True, default='')
    country_correspondence_residence = serializers.CharField(required=False, allow_blank=True, default='')
    street_correspondence_residence = serializers.CharField(required=False, allow_blank=True, default='')
    house_number_correspondence_residence = serializers.CharField(required=False, allow_blank=True, default='')
    flat_number_correspondence_residence = serializers.CharField(required=False, allow_blank=True, default='')
    mobile_number_correspondence_residence = serializers.CharField(required=False, allow_blank=True, default='')
    correspondence_address = serializers.CharField(required=False, allow_blank=True, default='')
    tax_office = serializers.CharField(required=False, allow_blank=True, default='')
    annual_settlement_address = serializers.CharField(required=False, allow_blank=True, default='')
    nfz_branch = serializers.CharField(required=False, allow_blank=True, default='')
    id_data = serializers.CharField(required=False, allow_blank=True, default='')
    id_given_by = serializers.CharField(required=False, allow_blank=True, default='')
    id_date = serializers.CharField(required=False, allow_blank=True, default='')
    approved = serializers.BooleanField(default=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(instance.id)
        return representation

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance = CustomUser.objects.get(email=user_data.get('email', ''))
        data_change_request = DataChangeRequest.objects.create(user=user_instance, **validated_data)
        return data_change_request
