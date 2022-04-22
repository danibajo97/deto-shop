# Generated by Django 3.2.7 on 2022-03-04 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_alter_orderproduct_total_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='total_paid',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product_price',
            field=models.FloatField(default=359),
            preserve_default=False,
        ),
    ]
