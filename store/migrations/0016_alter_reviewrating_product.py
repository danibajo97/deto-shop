# Generated by Django 3.2.7 on 2022-02-23 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_alter_variation_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
    ]
