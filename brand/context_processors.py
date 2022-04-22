from .models import Brand


def menu_brands(request):
    brand_links = Brand.objects.all()
    return dict(brand_links=brand_links)
