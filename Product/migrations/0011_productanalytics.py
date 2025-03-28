# Generated by Django 4.2.7 on 2025-01-26 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0010_alter_product_images_alter_product_bar_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0)),
                ('analytic_type', models.CharField(choices=[('impression', 'Impression'), ('view', 'View'), ('click', 'Click'), ('like', 'Like'), ('share', 'Share')], default='impression', max_length=20)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_insights', to='Product.product')),
            ],
        ),
    ]
