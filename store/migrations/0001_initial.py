# Generated by Django 3.2.7 on 2022-01-26 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('brand', '0001_initial'),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Color')),
                ('color_code', models.CharField(max_length=100, verbose_name='Código del Color')),
            ],
            options={
                'verbose_name': 'Color',
                'verbose_name_plural': 'Colores',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('label', models.CharField(blank=True, choices=[('sale', 'sale'), ('new', 'new'), ('promotion', 'promotion'), ('stockout', 'stockout')], max_length=10, null=True, verbose_name='Etiqueta')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 999999.99.'}}, help_text='Maximum 99999.99', max_digits=7, verbose_name='Regular price')),
                ('discount_percentage', models.PositiveIntegerField(blank=True, default=0)),
                ('product_image', models.ImageField(upload_to='static/img/products')),
                ('alt_text', models.CharField(max_length=200)),
                ('stock', models.IntegerField(blank=True)),
                ('is_available', models.BooleanField(default=True)),
                ('is_trending', models.BooleanField(default=False)),
                ('is_topSelling', models.BooleanField(default=False)),
                ('logo_image', models.ImageField(blank=True, upload_to='static/img/products_logo')),
                ('logo_altText', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Tamaño')),
            ],
            options={
                'verbose_name': 'Tamaño',
                'verbose_name_plural': 'Tamaños',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Producto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Lista de Deseos',
                'verbose_name_plural': 'Lista de Deseos',
            },
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.ImageField(max_length=255, upload_to='store/products')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.size')),
            ],
            options={
                'verbose_name': 'Variación',
                'verbose_name_plural': 'Variaciones',
            },
        ),
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=100)),
                ('review', models.TextField(blank=True, max_length=300)),
                ('rating', models.IntegerField()),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Clasificación',
                'verbose_name_plural': 'Clasificaciones',
            },
        ),
    ]
