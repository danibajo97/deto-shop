# Generated by Django 3.2.7 on 2022-02-28 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20220228_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]