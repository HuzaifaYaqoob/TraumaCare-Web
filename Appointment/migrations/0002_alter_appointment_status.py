# Generated by Django 4.1.5 on 2024-06-03 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Booked', 'Booked'), ('Confirmed', 'Confirmed'), ('Finished', 'Finished'), ('Cancelled', 'Cancelled')], default='Pending', max_length=999),
        ),
    ]