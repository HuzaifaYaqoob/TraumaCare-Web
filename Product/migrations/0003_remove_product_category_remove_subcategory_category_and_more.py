# Generated by Django 4.1.5 on 2025-01-02 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_productimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='category',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ManyToManyField(null=True, related_name='product_category_sub_categories', to='Product.productcategory'),
        ),
    ]