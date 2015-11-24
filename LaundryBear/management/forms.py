from django import forms
from database.models import Service, Price, LaundryShop, Transaction
from LaundryBear.forms import LoginForm


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 5})}


class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['laundry_shop', 'service', 'price', 'duration']


class LaundryShopForm(forms.ModelForm):
    class Meta:
        model = LaundryShop
        fields = ['barangay', 'building', 'city', 'contact_number',
                  'days_open', 'email', 'hours_open', 'name', 'province',
                  'street', 'website']


class AdminLoginForm(LoginForm):
    def clean(self):
        cleaned_data = super(AdminLoginForm, self).clean()
        user = cleaned_data.get('user')

        if not user.is_staff:
            raise forms.ValidationError('You have no power here.')


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['request_date']
