# Generated by Django 4.1.5 on 2024-12-20 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0023_alter_doctoronlineavailability_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='working_since',
            field=models.DateField(null=True),
        ),
    ]