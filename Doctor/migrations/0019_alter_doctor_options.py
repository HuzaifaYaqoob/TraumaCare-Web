# Generated by Django 4.1.5 on 2024-06-28 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0018_doctor_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'permissions': [('can_view_task', 'Can view task'), ('can_edit_task', 'Can edit task'), ('can_delete_task', 'Can delete task')]},
        ),
    ]
