# Generated by Django 5.0.1 on 2024-02-28 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_holidaytype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
        ),
    ]
