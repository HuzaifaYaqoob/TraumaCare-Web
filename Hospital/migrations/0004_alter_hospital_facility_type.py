# Generated by Django 4.1.5 on 2023-07-26 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0003_alter_hospital_options_alter_hospital_facility_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='facility_type',
            field=models.CharField(choices=[('Hospital', 'Hospital'), ('Private_Clinic', 'Private Clinic')], default='Hospital', max_length=50),
        ),
    ]