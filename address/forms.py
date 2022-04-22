from django import forms

from .models import Address


# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'phone_number', 'street_address', 'apartment_address', 'city', 'state', 'note_address', 'country', 'zip',
            'status')

    def __init__(self, *args, **kwargs):
        super(AddressBookForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-check-input'
