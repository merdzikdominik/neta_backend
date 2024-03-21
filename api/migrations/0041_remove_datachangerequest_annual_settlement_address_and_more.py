# Generated by Django 5.0.1 on 2024-03-21 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_alter_datachangerequest_city_correspondence_residence_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datachangerequest',
            name='annual_settlement_address',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='city_correspondence_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='city_permanent_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='city_second_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='correspondence_address',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='country_correspondence_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='country_permanent_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='country_second_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='flat_number_correspondence_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='flat_number_permanent_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='flat_number_second_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='house_number_correspondence_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='house_number_permanent_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='house_number_second_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='mobile_number_correspondence_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='mobile_number_permanent_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='mobile_number_second_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='municipal_commune_correspondence_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='municipal_commune_permanent_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='municipal_commune_second_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='post_correspondence_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='post_permanent_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='post_second_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='postal_code_correspondence_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='postal_code_permanent_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='postal_code_second_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='street_correspondence_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='street_permanent_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='street_second_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='tax_office',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='voivodeship_correspondence_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='voivodeship_permanent_residence',
        ),
        migrations.RemoveField(
            model_name='datachangerequest',
            name='voivodeship_second_residence',
        ),
    ]
