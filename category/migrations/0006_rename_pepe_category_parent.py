# Generated by Django 3.2.7 on 2022-02-17 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0005_auto_20220217_1250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='pepe',
            new_name='parent',
        ),
    ]
