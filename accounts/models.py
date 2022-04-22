from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.html import mark_safe
from django_countries.fields import CountryField
from insomnio.settings import STATIC_URL


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            # normalize the user entered email, if it is a big letter to small letter
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)  # it is a inbuilt function
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='static/img/profile',
                                        default='static/img/profile/index.png')
    is_seller = models.BooleanField(default=False)
    is_visitor = models.BooleanField(default=False)
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name} / {self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def image_tag(self):
        if self.profile_picture:
            return mark_safe(
                '<img src="%s" width="50" height="50" style="border-radius:50px;" />' % self.profile_picture.url)

    class Meta:
        verbose_name_plural = 'Usuarios'
        verbose_name = 'Usuario'
