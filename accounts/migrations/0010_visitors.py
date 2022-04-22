# Generated by Django 3.2.7 on 2022-03-05 04:16

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_account_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone_number', models.CharField(max_length=50)),
                ('street_address', models.CharField(max_length=100, verbose_name='Calle')),
                ('note_address', models.CharField(blank=True, max_length=100, verbose_name='Notas Adicionales de la Direccion')),
                ('apartment_address', models.CharField(max_length=100, verbose_name='Apartamento')),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(blank=True, max_length=20)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='País')),
                ('zip', models.CharField(max_length=100, verbose_name='Zip')),
            ],
            options={
                'verbose_name': 'Visitante',
                'verbose_name_plural': 'Visitantes',
            },
        ),
    ]