# Generated by Django 3.2.7 on 2022-02-28 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_variation_stock'),
        ('cart', '0005_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variations',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.variation'),
        ),
    ]
