# Generated by Django 3.2.7 on 2022-01-29 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20220127_1301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='coupon',
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
    ]
