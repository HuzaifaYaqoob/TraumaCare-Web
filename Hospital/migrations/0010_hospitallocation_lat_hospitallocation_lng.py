# Generated by Django 4.1.5 on 2024-12-19 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0009_hospital_is_onboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitallocation',
            name='lat',
            field=models.CharField(default='', max_length=999, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='hospitallocation',
            name='lng',
            field=models.CharField(default='', max_length=999, verbose_name='Longitude'),
        ),
    ]