# Generated by Django 5.0.1 on 2024-03-22 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_datachangerequest_city_correspondence_residence_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='datachangerequest',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
