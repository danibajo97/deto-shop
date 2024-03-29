# Generated by Django 3.2.7 on 2022-01-27 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address_type',
        ),
        migrations.RemoveField(
            model_name='address',
            name='phone',
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='address',
            name='note_address',
            field=models.CharField(blank=True, max_length=100, verbose_name='Notas Adicionales de la Direccion'),
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
