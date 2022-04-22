from brand.models import Brand
from django.db import models
from django.utils.html import mark_safe
from django.urls import reverse


class Subscribe(models.Model):
    email = models.EmailField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Subscripciones'
        verbose_name = 'Subscritos'


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=150)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}, {self.title}'

    class Meta:
        verbose_name_plural = 'Mensajes'
        verbose_name = 'Mensaje'


class Blog(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/img/blog')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True) 
    body = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.brand.title}, {self.title}'

    class Meta:
        verbose_name_plural = 'Blogs'
        verbose_name = 'Blog'

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)
        
    def get_url(self):
        return reverse('blog_article', args=[self.slug])
