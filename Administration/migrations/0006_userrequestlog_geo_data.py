# Generated by Django 4.1.5 on 2024-07-02 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0005_userrequestlog_city_userrequestlog_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequestlog',
            name='geo_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]