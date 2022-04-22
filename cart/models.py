from accounts.models import Account
from django.db import models
from store.models import Product, Variation


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    class Meta:
        verbose_name_plural = 'Carritos'
        verbose_name = 'Carrito'


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ForeignKey(Variation, on_delete=models.CASCADE)  # relation with varinat
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Cupón')

    def sub_total(self):
        if self.variations.discount_price:
            the_price = self.variations.discount_price * self.quantity
            return round(the_price, 2)
        else:
            return self.variations.price * self.quantity

    def __str__(self):
        if self.variations.color and self.variations.size:
            return f'{self.quantity} of {self.product.name}, Color: {self.variations.color.name}, Size: {self.variations.size.name}'
        elif self.variations.color:
            return f'{self.quantity} of {self.product.name}, Color: {self.variations.color.name}'
        elif self.variations.size:
            return f'{self.quantity} of {self.variations.product}, Size: {self.variations.size.name}'
        else:
            return f'{self.quantity} of {self.product.name}'

    class Meta:
        verbose_name_plural = 'Productos agregados al carrito'
        verbose_name = 'Producto agregado al carrito'


class Coupon(models.Model):
    code = models.CharField(max_length=15, verbose_name='Código')
    amount = models.FloatField(verbose_name='Monto')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'Coupón'
        verbose_name = 'Coupón'
