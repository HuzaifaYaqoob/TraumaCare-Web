# Generated by Django 4.1.5 on 2024-12-18 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_task', to=settings.AUTH_USER_MODEL),
        ),
    ]