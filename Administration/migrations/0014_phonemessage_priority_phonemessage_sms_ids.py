# Generated by Django 4.1.5 on 2024-08-17 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0013_smsservicekey_key_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonemessage',
            name='priority',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='phonemessage',
            name='sms_ids',
            field=models.TextField(blank=True, null=True),
        ),
    ]
