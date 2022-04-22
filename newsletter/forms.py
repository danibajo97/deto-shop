from django import forms

from .models import Subscribe, Contact


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email', ]

    def clean(self):
        email = self.cleaned_data['email']
        if Subscribe.objects.filter(email=email).exists():
            raise forms.ValidationError('You are already subscribed!')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'title', 'body']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['title'].widget.attrs['placeholder'] = 'Title'
        self.fields['body'].widget.attrs['placeholder'] = 'Body'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
