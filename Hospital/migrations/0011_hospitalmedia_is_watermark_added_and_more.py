# Generated by Django 4.1.5 on 2024-12-21 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0010_hospitallocation_lat_hospitallocation_lng'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalmedia',
            name='is_watermark_added',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='hospitalmedia',
            name='file',
            field=models.FileField(help_text='Whenever change Image, You must uncheck "Is Watermark Added"', upload_to='Hospital/Files/%Y-%m'),
        ),
    ]