# Generated by Django 4.1.5 on 2024-06-03 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0014_doctorreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctoreducation',
            name='degree_name',
            field=models.CharField(default='', max_length=999),
        ),
    ]
