# Generated by Django 4.1.5 on 2024-06-04 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0004_alter_hospital_facility_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='slug',
            field=models.TextField(default=''),
        ),
    ]
