# Generated by Django 3.2.7 on 2022-03-04 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_alter_orderproduct_total_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_items',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
            preserve_default=False,
        ),
    ]
