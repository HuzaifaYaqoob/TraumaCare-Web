# Generated by Django 4.1.5 on 2024-12-22 16:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0008_staffrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffrole',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_roles', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]