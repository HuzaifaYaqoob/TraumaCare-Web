# Generated by Django 4.1.5 on 2025-01-05 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0008_subcategory_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='treatmenttype',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Product/TreatmentType/%Y-%m'),
        ),
    ]
