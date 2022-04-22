# Generated by Django 3.2.7 on 2022-03-05 04:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_visitors'),
        ('orders', '0026_remove_orderproduct_total_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='visitors',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.visitors'),
        ),
    ]