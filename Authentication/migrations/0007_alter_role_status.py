# Generated by Django 4.1.5 on 2024-12-21 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0006_role_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=255),
        ),
    ]
