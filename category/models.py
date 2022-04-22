from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField


class Category(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=51, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='static/img/categories')
    image_large = models.ImageField(upload_to='static/img/categories', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.name]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)

    def toJSON(self):
        item = model_to_dict(self)
        item['parent'] = self.parent
        item['name'] = self.name
        item['slug'] = self.slug
        item['is_active'] = self.is_active
        item['description'] = self.description
        item['image'] = self.get_image()
        item['created_at'] = self.created_at.strftime('%Y-%m-%d')
        item['updated_at'] = self.updated_at.strftime('%Y-%m-%d')
        return item