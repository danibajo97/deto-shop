from django.urls import path, include
from . import views

urlpatterns = [
    # My AddressBook
    path('my_addressbook/', views.my_addressbook, name='my_addressbook'),
    path('add_address/', views.save_address, name='add_address'),
    path('activate_address/', views.activate_address, name='activate_address'),
    path('update_address/<int:id>', views.update_address, name='update_address'),
    path('delete_address/<int:id>', views.delete_address, name='delete_address'),
]
