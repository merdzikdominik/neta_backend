# Generated by Django 5.0.1 on 2024-03-13 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_customuser_annualsettlementaddress_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='date',
            new_name='idDate',
        ),
    ]