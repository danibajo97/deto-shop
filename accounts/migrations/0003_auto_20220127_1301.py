# Generated by Django 3.2.7 on 2022-01-27 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='static/img/profile'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
