# Generated by Django 4.1.5 on 2024-07-03 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0002_alter_appointment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Booked', 'Booked'), ('Confirmed', 'Confirmed'), ('Finished', 'Finished'), ('Cancelled', 'Cancelled'), ('Expired', 'Expired')], default='Pending', max_length=999),
        ),
    ]