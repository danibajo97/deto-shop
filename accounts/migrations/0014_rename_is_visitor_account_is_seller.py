# Generated by Django 3.2.7 on 2022-03-14 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_account_profile_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='is_visitor',
            new_name='is_seller',
        ),
    ]