from accounts.models import Account
from brand.models import Brand
from category.models import Category
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.db.models import Max, Min
from django.forms import model_to_dict
from django.urls import reverse
from django.utils.html import mark_safe
from store.get_current_user import current_request

LABEL_CHOICES = (
    ('sale', 'sale'),
    ('new', 'new'),
    ('hot', 'hot'),
)

VARIANTS = (
    ('None', 'None'),
    ('Size', 'Size'),
    ('Color', 'Color'),
    ('Size-Color', 'Size-Color'),
)


class Product(models.Model):
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    brand = models.ForeignKey(Brand, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    description = RichTextUploadingField()
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = 'Productos'
        verbose_name = 'Producto'

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        item['name'] = self.name
        item['brand'] = self.brand.toJSON()
        item['slug'] = self.slug
        item['description'] = self.description
        item['variant'] = {'id': self.variant, 'option': self.get_variant_display()}
        item['is_available'] = self.is_available
        item['created_at'] = self.created_at.strftime('%Y-%m-%d')
        item['updated_at'] = self.updated_at.strftime('%Y-%m-%d')
        return item

    def get_url(self):
        return reverse('product_detail', args=[self.brand.slug, self.category.slug, self.slug])

    def get_variation(self):
        variations = Variation.objects.filter(product=self, is_active=True).first()
        return variations

    def get_variation_all(self):
        variations_all = Variation.objects.filter(product=self, is_active=True)
        return variations_all

    def get_product_size(self):
        products = Variation.objects.filter(product=self, is_active=True)
        sizes = []
        products_size = []
        for product in products:
            if product.size not in sizes:
                sizes.append(product.size)
        for size in sizes:
            product = Variation.objects.filter(product=self, is_active=True, size=size).first()
            products_size.append(product)
        return products_size

    def get_product_color(self):
        products = Variation.objects.filter(product=self, is_active=True)
        colors = []
        products_color = []
        for product in products:
            if product.color not in colors:
                colors.append(product.color)
        for color in colors:
            product = Variation.objects.filter(product=self, is_active=True, color=color).first()
            products_color.append(product)
        return products_color

    def average_rating(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def __str__(self):
        return self.name

    def get_min_price(self):
        variations = self.get_variation_all()
        price_min = variations.aggregate(Min('price'))
        min_price = price_min['price__min']
        for item in variations:
            if item.discount_price is not None and item.discount_price < min_price:
                min_price = item.discount_price
        return min_price

    def get_max_price(self):
        variations = self.get_variation_all()
        price_max = variations.aggregate(Max('price'))
        max_price = price_max['price__max']
        for item in variations:
            if item.discount_price is not None and item.discount_price > max_price:
                max_price = item.discount_price
        return max_price

    def is_in_wishlist(self):
        user = current_request()
        wishlist = Wishlist.objects.filter(user=user.user, product=self)
        if wishlist:
            return True
        else:
            return False


class Image(models.Model):
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='static/img/store')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)

    def get_image(self):
        if self.image:
            return self.image.url

    def toJSON(self):
        item = model_to_dict(self)
        item['title'] = self.title
        item['image'] = self.get_image()
        return item


class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['name'] = self.name
        item['code'] = self.code
        item['slug'] = self.slug
        return item

    def color_tag(self):
        if self.code is not None:
            return mark_safe(
                '<div style="width:30px; height:30px; border-style:solid; background-color:%s"></div>' % self.code)
        else:
            return ""


class SizeType(models.Model):
    type = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.type


class Size(models.Model):
    type = models.ForeignKey(SizeType, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['name'] = self.name
        item['code'] = self.code
        item['slug'] = self.slug
        return item


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=10, verbose_name='Etiqueta', blank=True, null=True)
    description = RichTextUploadingField()
    is_active = models.BooleanField(default=True)
    image = models.ManyToManyField(Image, max_length=255, blank=True)
    price = models.DecimalField(
        verbose_name="Regular price",
        help_text="Maximum 99999.99",
        error_messages={
            "name": {
                "max_length": "The price must be between 0 and 999999.99.",
            },
        },
        max_digits=7,
        decimal_places=2,
    )
    discount_percentage = models.PositiveIntegerField(default=0, blank=True)
    stock = models.PositiveIntegerField(default=1, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.color and self.size:
            return f'{self.product}, Color: {self.color.name}, Size: {self.size.name}'
        elif self.color:
            return f'{self.product}, Color: {self.color.name}'
        elif self.size:
            return f'{self.product}, Size: {self.size.name}'
        else:
            return f'{self.product}'

    def toJSON(self):
        item = model_to_dict(self)
        item['product'] = self.product.toJSON()
        item['color'] = self.color.toJSON()
        item['size'] = self.size.toJSON()
        item['label'] = {'id': self.label, 'option': self.get_label_display()}
        item['description'] = self.description
        item['is_active'] = self.is_active
        item['image'] = self.image.toJSON()
        item['price'] = self.price
        item['discount_percentage'] = self.discount_percentage
        item['stock'] = self.stock
        item['created_date'] = self.created_date.strftime('%Y-%m-%d')
        item['updated_at'] = self.updated_at.strftime('%Y-%m-%d')
        return item

    def discountPrice(self):
        if self.discount_percentage > 0:
            the_price = self.price - ((self.price * self.discount_percentage) / 100)
            return round(the_price, 2)

    discount_price = property(discountPrice)

    def image_tag(self):
        img = self.image.all().first()
        if img is not None:
            return mark_safe('<img src="%s" width="50" height="50" />' % img.image.url)
        else:
            return ""

    def image_first(self):
        img_first = self.image.all().first()
        if img_first is not None:
            return img_first.image.url
        else:
            return ""

    def image_last(self):
        img_last = self.image.all().last()
        if img_last is not None:
            return img_last.image.url
        else:
            return ""

    def image_home_all(self):
        img_all = self.image.all()
        if img_all is not None:
            return img_all
        else:
            return ""

    def slug(self):
        if self.color and self.size:
            return f'{self.product.slug}-{self.color.slug}-{self.size.slug}'
        elif self.color:
            return f'{self.product.slug}-{self.color.slug}'
        elif self.size:
            return f'{self.product.slug}-{self.size.slug}'
        else:
            return f'{self.product.slug}'

    slug = property(slug)

    def get_url(self):
        return reverse('variation_detail',
                       args=[self.product.brand.slug, self.product.category.slug, self.product.slug, self.slug])

    class Meta:
        verbose_name_plural = 'Variaciones'
        verbose_name = 'Variación'


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    review = models.TextField(max_length=1500)
    rating = models.FloatField(default=1, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name}, {self.subject}'

    class Meta:
        verbose_name_plural = 'Reseñas'
        verbose_name = 'Reseña'


# WishList
class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Usuario')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')

    class Meta:
        verbose_name_plural = 'Lista de Deseos'
        verbose_name = 'Lista de Deseos'

    def __str__(self):
        return self.product.name


# class CompareProducts(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Usuario')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
#     variations = models.ForeignKey(Variation, on_delete=models.CASCADE)  # relation with varinat
# 
#     class Meta:
#         verbose_name_plural = 'Comparaciones'
#         verbose_name = 'Comparación'
# 
#     def __str__(self):
#         return self.product.name
