# Generated by Django 4.1.5 on 2024-06-29 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0005_blogposttopic'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogmedia',
            name='is_thumbnail_generated',
            field=models.BooleanField(default=False),
        ),
    ]
