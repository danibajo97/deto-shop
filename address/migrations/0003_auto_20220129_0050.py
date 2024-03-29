# Generated by Django 3.2.7 on 2022-01-29 06:50

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_auto_20220127_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='País'),
        ),
    ]
