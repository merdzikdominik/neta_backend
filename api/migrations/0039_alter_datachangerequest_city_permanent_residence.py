# Generated by Django 5.0.1 on 2024-03-21 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_datachangerequest_annual_settlement_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datachangerequest',
            name='city_permanent_residence',
            field=models.TextField(blank=True, default='', max_length=50),
        ),
    ]
