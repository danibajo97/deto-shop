# Generated by Django 3.2.7 on 2022-03-05 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_account_is_visitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(blank=True, default='static/img/profile/index.png', null=True, upload_to='static/img/profile'),
        ),
    ]