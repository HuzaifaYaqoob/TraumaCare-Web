# Generated by Django 4.1.5 on 2023-06-08 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0002_doctor24by7'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]