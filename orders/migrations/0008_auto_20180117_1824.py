# Generated by Django 2.0 on 2018-01-17 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20180117_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
        ),
    ]