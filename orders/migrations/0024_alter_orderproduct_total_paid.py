# Generated by Django 3.2.7 on 2022-03-04 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_alter_orderproduct_total_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='total_paid',
            field=models.FloatField(default=240),
            preserve_default=False,
        ),
    ]
