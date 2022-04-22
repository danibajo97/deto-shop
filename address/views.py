from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import AddressBookForm
from .models import Address


# My AddressBook
@login_required(login_url='login')
def my_addressbook(request):
    title = 'Address Book'
    addbook = Address.objects.filter(user=request.user).order_by('-id')
    context = {
        'addbook': addbook,
        'title': title,
    }
    return render(request, 'accounts/addressbook.html', context)


# Save addressbook
@login_required(login_url='login')
def save_address(request):
    title = 'Add Address'
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                Address.objects.update(status=False)
            saveForm.save()
            messages.success(request, "Data has been saved")
            return redirect('my_addressbook')
        else:
            messages.error(request, "Invalid Inputs")
    form = AddressBookForm
    context = {'form': form,
               'title': title}
    return render(request, 'accounts/add_address.html', context)


# Activate address
@login_required(login_url='login')
def activate_address(request):
    a_id = str(request.GET['id'])
    Address.objects.update(status=False)
    Address.objects.filter(id=a_id).update(status=True)
    return JsonResponse({'bool': True})


# Update addressbook
@login_required(login_url='login')
def update_address(request, id):
    title = 'Update Address'
    address = Address.objects.get(pk=id)
    if request.method == 'POST':
        form = AddressBookForm(request.POST, instance=address)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                Address.objects.update(status=False)
            saveForm.save()
            messages.success(request, "Data has been saved")
            return redirect('my_addressbook')
        else:
            messages.error(request, "Invalid Inputs")
    form = AddressBookForm(instance=address)
    context = {'form': form,
               'title': title}
    return render(request, 'accounts/update_address.html', context)


@login_required(login_url='login')
def delete_address(request, id):
    address = Address.objects.get(pk=id)
    address.delete()
    first_address = Address.objects.filter(user=request.user).first()
    if first_address:
        first_address.status = True
        first_address.save()
    messages.success(request, "Data has been deleted")
    return redirect('my_addressbook')
