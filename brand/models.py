from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from accounts.models import Account


# Brand
class Brand(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Marca')
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to="static/img/brands", verbose_name='Imagen')
    image_large = models.ImageField(upload_to="static/img/brands", blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Es activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    instagram = models.CharField(max_length=500, blank=True)
    facebook = models.CharField(max_length=500, blank=True)
    telegram = models.CharField(max_length=500, blank=True)
    whatsapp = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name_plural = 'Marcas'
        verbose_name = 'Marca'

    def get_url(self):
        return reverse('products_by_brand', args=[self.slug])

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}, Brand: {self.title}'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        
    def toJSON(self):
        item = model_to_dict(self)
        item['title'] = self.title
        item['slug'] = self.slug
        item['image'] = self.get_image()
        item['is_active'] = self.is_active
        item['created_at'] = self.created_at.strftime('%Y-%m-%d')
        item['updated_at'] = self.updated_at.strftime('%Y-%m-%d')
        return item
