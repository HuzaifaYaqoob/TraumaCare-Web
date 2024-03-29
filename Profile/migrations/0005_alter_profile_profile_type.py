# Generated by Django 4.1.5 on 2023-07-26 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0004_alter_profile_profile_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_type',
            field=models.CharField(choices=[('Patient', 'General'), ('Doctor', 'Doctor'), ('Hospital', 'Hospital'), ('Pharmacy', 'Pharmacy'), ('Lab', 'Lab'), ('Private_Clinic', 'Private_Clinic')], default='Patient', max_length=15),
        ),
    ]
