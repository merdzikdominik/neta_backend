# Generated by Django 5.0.1 on 2024-03-21 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_alter_datachangerequest_id_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datachangerequest',
            name='id_data',
            field=models.CharField(blank=True, default=None, max_length=30),
        ),
        migrations.AlterField(
            model_name='datachangerequest',
            name='id_given_by',
            field=models.CharField(blank=True, default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='datachangerequest',
            name='nfz_branch',
            field=models.CharField(blank=True, default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='datachangerequest',
            name='surname',
            field=models.CharField(blank=True, default=None, max_length=20),
        ),
    ]
