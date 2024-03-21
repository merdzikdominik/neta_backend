# Generated by Django 5.0.1 on 2024-03-21 10:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_alter_datachangerequest_id_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datachangerequest',
            name='id_data',
            field=models.TextField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='datachangerequest',
            name='id_date',
            field=models.TextField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='datachangerequest',
            name='id_given_by',
            field=models.TextField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='datachangerequest',
            name='nfz_branch',
            field=models.TextField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='datachangerequest',
            name='surname',
            field=models.TextField(blank=True, default='', max_length=20),
        ),
    ]
