from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import SubscribeForm, ContactForm
from .models import Blog


def subscribe(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription Successful.')
            return redirect(url)
        else:
            messages.error(request, 'You are already subscribed!')
            return redirect(url)


def contact_me(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message has been sent. Thank you for contacting us.')
            return redirect('contact_me')

        else:
            form = ContactForm()
            messages.error(request, 'Message not sent! Please try again later.')
            return render(request, 'contact-us.html', {'form': form})
    else:
        form = ContactForm()
        return render(request, 'contact-us.html', {'form': form})


def blog(request):
    blogs = Blog.objects.filter(is_active=True)
    recent_blogs = Blog.objects.filter(is_active=True).order_by("-updated_at")[0:4]
    context = {
        'blogs': blogs,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'blog.html', context)


def blog_article(request, blog_slug):
    selected_blog = Blog.objects.get(slug=blog_slug, is_active=True)
    recent_blogs = Blog.objects.filter(is_active=True).order_by("-updated_at")[0:4]
    context = {
        'selected_blog': selected_blog,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'blog-article.html', context)


def about_us(request):
    return render(request, 'about-us.html')
