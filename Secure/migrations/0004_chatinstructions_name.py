# Generated by Django 4.1.5 on 2024-06-10 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Secure', '0003_chatinstructions'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatinstructions',
            name='name',
            field=models.CharField(default='', max_length=999),
        ),
    ]
