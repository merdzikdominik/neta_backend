from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from knox.models import AuthToken

class Scheduler(models.Model):
    dateFrom = models.DateField()
    dateTo = models.DateField()

    def __str__(self):
        return f'Urlop od {self.dateFrom} do {self.dateTo}'


class HolidayPlan(models.Model):
    dateFrom = models.DateField()
    dateTo = models.DateField()

    def __str__(self):
        return f"Okres planu urlopowego: {self.dateFrom} do {self.dateTo}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        first_name = extra_fields.pop('first_name', '')
        last_name = extra_fields.pop('last_name', '')

        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    employment_start_date = models.DateField(blank=True, null=True)
    employment_end_date = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=30, blank=True, null=True)
    education = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    user_residence_data = models.JSONField(blank=True, null=True)
    correspondence_address = models.CharField(max_length=100, blank=True, null=True)
    tax_office = models.CharField(max_length=100, blank=True, null=True)
    annual_settlement_address = models.CharField(max_length=100, blank=True, null=True)
    nfz_branch = models.CharField(max_length=100, blank=True, null=True)
    id_data = models.CharField(max_length=100, blank=True, null=True)
    id_given_by = models.CharField(max_length=100, blank=True, null=True)
    id_date = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postalCode = models.CharField(max_length=100, blank=True, null=True)
    post = models.CharField(max_length=100, blank=True, null=True)
    municipalCommune = models.CharField(max_length=100, blank=True, null=True)
    voivodeship = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    house_number = models.CharField(max_length=100, blank=True, null=True)
    flat_number = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class HolidayRequest(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    difference_in_days = models.IntegerField()
    selected_holiday_type = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    color_hex = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return f'Urlop od {self.start_date} do {self.end_date} użytkownika {self.user.email}'


class HolidayType(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class Notification(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label