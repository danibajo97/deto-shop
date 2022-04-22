from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('contact/', views.contact_me, name='contact_me'),
    path('about-us/', views.about_us, name='about_us'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:blog_slug>/', views.blog_article, name='blog_article')
]