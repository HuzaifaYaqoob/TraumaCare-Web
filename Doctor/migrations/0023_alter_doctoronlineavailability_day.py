# Generated by Django 4.1.5 on 2024-12-19 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0022_doctorwithhospital_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctoronlineavailability',
            name='day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='', max_length=20),
        ),
    ]
