from django.forms import ModelForm
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


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['client', 'status', 'request_date', 'delivery_date']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['price', 'transaction', 'pieces']
