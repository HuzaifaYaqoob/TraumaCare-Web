# Generated by Django 4.1.5 on 2024-08-17 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0009_hospital_is_onboard'),
        ('Doctor', '0022_doctorwithhospital_created_at_and_more'),
        ('ChatXpo', '0008_remove_chatmessage_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='doctor_messages', to='Doctor.doctor')),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='hospital_messages', to='Hospital.hospital')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='message_contents', to='ChatXpo.chatmessage')),
            ],
        ),
    ]
