# Generated by Django 3.2.7 on 2022-03-16 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_compareproducts_variations'),
        ('cart', '0010_auto_20220304_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='variations',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
    ]
