# Generated by Django 3.2.7 on 2022-02-28 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_reviewrating_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='size',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]