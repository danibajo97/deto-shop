# Generated by Django 3.2.7 on 2022-02-12 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20220131_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=1.0, max_digits=1),
        ),
    ]