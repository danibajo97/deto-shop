# Generated by Django 3.2.7 on 2022-02-23 17:17

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20220223_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
