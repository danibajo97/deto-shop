# Generated by Django 3.2.7 on 2022-03-05 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0028_remove_order_visitors'),
        ('accounts', '0010_visitors'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Visitors',
        ),
    ]
