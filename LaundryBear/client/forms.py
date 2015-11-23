from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from database.models import UserProfile, Price, Rating, Order, Transaction

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'username', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['client']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['price', 'transaction', 'pieces']


class AddressForm(Form):
    province = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50, required=True)
    barangay = forms.CharField(max_length=50)
    street = forms.CharField(max_length=50, required=True)
    building = forms.CharField(max_length=50, required=True)


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = ['client', 'request_date', 'status']
