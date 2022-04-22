from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe


# Banner
class Slides(models.Model):
    caption1 = models.CharField(max_length=100, verbose_name='Título 1')
    caption2 = models.CharField(max_length=100, verbose_name='Título 2', blank=True, null=True)
    link = models.CharField(max_length=100)
    image = models.ImageField(help_text="Size: 1920x570", upload_to="static/img/slides", verbose_name='Imagen')
    is_active = models.BooleanField(default=True, verbose_name='Es Activo')

    class Meta:
        verbose_name_plural = 'Diapositivas'
        verbose_name = 'Diapositiva'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % self.image.url)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)
