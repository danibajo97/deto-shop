# Generated by Django 3.2.7 on 2022-03-04 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0025_alter_orderproduct_total_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='total_paid',
        ),
    ]
