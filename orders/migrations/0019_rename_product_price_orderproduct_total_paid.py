# Generated by Django 3.2.7 on 2022-03-04 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_auto_20220304_0136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='product_price',
            new_name='total_paid',
        ),
    ]
