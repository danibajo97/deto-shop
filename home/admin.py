from django.contrib import admin
from .models import Slides


class SlideAdmin(admin.ModelAdmin):
    list_display = ('caption1', 'caption2', 'image_tag')


admin.site.register(Slides, SlideAdmin)
