# Generated by Django 5.0.1 on 2024-03-14 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_rename_municipalcommune_customuser_municipal_commune_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]