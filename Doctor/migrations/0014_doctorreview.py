# Generated by Django 4.1.5 on 2024-06-01 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Doctor', '0013_remove_doctoreducation_practice_institute_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorReview',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('review', models.TextField(default='')),
                ('rating', models.PositiveIntegerField(default=0)),
                ('recommended_rating', models.PositiveIntegerField(default=0)),
                ('checkup_rating', models.PositiveIntegerField(default=0)),
                ('clinical_environment_rating', models.PositiveIntegerField(default=0)),
                ('staff_behaviour_rating', models.PositiveIntegerField(default=0)),
                ('secret_review', models.TextField(default='')),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_reviews', to='Doctor.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]