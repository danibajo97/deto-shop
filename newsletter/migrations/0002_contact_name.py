# Generated by Django 3.2.7 on 2022-03-10 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='name',
            field=models.CharField(default='Daniel', max_length=200),
            preserve_default=False,
        ),
    ]