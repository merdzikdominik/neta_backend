# Generated by Django 5.0.1 on 2024-04-16 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_alter_holidayrequestplan_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holidayrequestplan',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]