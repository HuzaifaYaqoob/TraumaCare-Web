# Generated by Django 4.1.5 on 2024-07-18 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0008_remove_hospitallocation_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='is_onboard',
            field=models.BooleanField(default=False),
        ),
    ]
