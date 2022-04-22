# Generated by Django 3.2.7 on 2022-03-04 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20220304_0125'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='total_paid',
            field=models.DecimalField(decimal_places=2, default=350, error_messages={'name': {'max_length': 'The price must be between 0 and 999999.99.'}}, help_text='Maximum 99999.99', max_digits=7, verbose_name='Regular price'),
            preserve_default=False,
        ),
    ]