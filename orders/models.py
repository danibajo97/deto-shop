from accounts.models import Account
from address.models import Address
from django.db import models
from store.models import Product, Variation

PAYMENT_CHOICES = (
    ('D', 'Domicilio'),
    ('P', 'Pagar al Recoger')
)


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_CHOICES, default='Domicilio', max_length=10)
    total_paid = models.DecimalField(
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
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}, Total Paid: {self.total_paid}'

    class Meta:
        verbose_name_plural = 'Pagos'
        verbose_name = 'Pago'


class Order(models.Model):
    STATUS = (
        ('New', 'Nuevo'),
        ('Accepted', 'Aceptado'),
        ('Completed', 'Completado'),
        ('Cancelled', 'Cancelado'),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    order_note = models.TextField(blank=True)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False, verbose_name='Recibido')
    refund_requested = models.BooleanField(default=False, verbose_name='Reembolso requerido')
    refund_granted = models.BooleanField(default=False, verbose_name='Reembolso Concedido')
    order_total = models.FloatField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}, Order: {self.order_number}'
    
    def get_ordersProducts_all(self):
        ordersProducts_all = OrderProduct.objects.filter(order=self)
        return ordersProducts_all

    class Meta:
        verbose_name_plural = 'Ordenes'
        verbose_name = 'Orden'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ForeignKey(Variation, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.variations.color and self.variations.size:
            return f'{self.quantity} of {self.product.name}, Color: {self.variations.color.name}, Size: {self.variations.size.name}'
        elif self.variations.color:
            return f'{self.quantity} of {self.product.name}, Color: {self.variations.color.name}'
        elif self.variations.size:
            return f'{self.quantity} of {self.product.name}, Size: {self.variations.size.name}'
        else:
            return f'{self.quantity} of {self.product.name}'

    def sub_total(self):
        if self.variations.discount_price:
            the_price = self.variations.discount_price * self.quantity
            return round(the_price, 2)
        else:
            return self.variations.price * self.quantity

    class Meta:
        verbose_name_plural = 'Productos Ordenados'
        verbose_name = 'Producto Ordenado'


# class Refund(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Pedido')
#     reason = models.TextField(verbose_name='Razones')
#     accepted = models.BooleanField(default=False, verbose_name='Aceptado')
#     email = models.EmailField(verbose_name='Correo')
# 
#     def __str__(self):
#         return f'{self.order.order_number}'
# 
#     class Meta:
#         verbose_name_plural = 'Reembolsos'
#         verbose_name = 'Reembolso'
