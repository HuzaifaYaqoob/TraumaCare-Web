# Generated by Django 4.1.5 on 2024-07-02 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0004_remove_userrequestlog_headers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequestlog',
            name='city',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
        migrations.AddField(
            model_name='userrequestlog',
            name='country',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
        migrations.AddField(
            model_name='userrequestlog',
            name='country_code',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
        migrations.AddField(
            model_name='userrequestlog',
            name='lat',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
        migrations.AddField(
            model_name='userrequestlog',
            name='lng',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
        migrations.AddField(
            model_name='userrequestlog',
            name='postal_code',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
    ]