# Generated by Django 4.1.5 on 2025-01-06 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0008_rename_is_thumbnail_generated_profile_is_watermark_added_and_more'),
        ('Appointment', '0004_appointment_is_sms_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentgroup',
            name='patient_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profile_appointments', to='Profile.profile'),
        ),
    ]
