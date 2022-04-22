from accounts.models import Account
from django.db import models
from django_countries.fields import CountryField


# Address
class Address(models.Model):
    user = models.ForeignKey(Account,
                             on_delete=models.CASCADE, verbose_name='Usuario')
    phone_number = models.CharField(max_length=50)
    street_address = models.CharField(max_length=100, verbose_name='Calle')
    note_address = models.CharField(max_length=100, verbose_name='Notas Adicionales de la Direccion', blank=True)
    apartment_address = models.CharField(max_length=100, verbose_name='Apartamento')
    city = models.CharField(max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = CountryField(blank=True, multiple=False, verbose_name='País')
    zip = models.CharField(max_length=100, verbose_name='Zip')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.street_address}, {self.apartment_address}, {self.city}'

    class Meta:
        verbose_name_plural = 'Dirección de Envíos'
        verbose_name = 'Dirección de Envío'

    def full_address(self):
        return f'{self.street_address}, {self.apartment_address}, {self.city}'
