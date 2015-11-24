from django import forms
from database.models import Rating, Service, Price, LaundryShop, Transaction, User, UserProfile
from LaundryBear.forms import LoginForm
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'username', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['client']


class ChangeUsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']
