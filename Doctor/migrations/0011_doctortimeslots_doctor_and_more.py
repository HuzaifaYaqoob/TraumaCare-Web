# Generated by Django 4.1.5 on 2024-05-31 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0010_remove_doctortimeslots_doctor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctortimeslots',
            name='doctor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_timeslots', to='Doctor.doctor'),
        ),
        migrations.AlterField(
            model_name='doctorwithhospital',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_hospital_timeslots', to='Doctor.doctor'),
        ),
    ]