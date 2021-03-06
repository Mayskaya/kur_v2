# Generated by Django 2.0 on 2017-12-15 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_address_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
        ),
        migrations.AddField(
            model_name='product_order',
            name='nmb',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='product_order',
            name='price_per_item',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
        ),
        migrations.AddField(
            model_name='product_order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
        ),
    ]
