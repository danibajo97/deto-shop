# Generated by Django 3.2.7 on 2022-02-21 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20220219_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='variant',
            field=models.CharField(choices=[('None', 'None'), ('Size', 'Size'), ('Color', 'Color'), ('Size-Color', 'Size-Color')], default='None', max_length=10),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, upload_to='static/img/store'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_product',
            field=models.ImageField(blank=True, upload_to='static/img/store'),
        ),
    ]
