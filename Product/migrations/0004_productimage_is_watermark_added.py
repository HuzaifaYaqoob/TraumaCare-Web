# Generated by Django 4.1.5 on 2025-01-02 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_remove_product_category_remove_subcategory_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='is_watermark_added',
            field=models.BooleanField(default=False),
        ),
    ]