# Generated by Django 3.2.7 on 2022-03-01 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0002_brand_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]