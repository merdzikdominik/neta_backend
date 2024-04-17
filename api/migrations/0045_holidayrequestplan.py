# Generated by Django 5.0.1 on 2024-04-16 10:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_datachangerequest_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='HolidayRequestPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('difference_in_days', models.IntegerField()),
                ('selected_holiday_type', models.CharField(max_length=255)),
                ('message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('color_hex', models.CharField(blank=True, max_length=7, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]