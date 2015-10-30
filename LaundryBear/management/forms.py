from django import forms

from database.models import Rating, Service, Price, LaundryShop


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 5})}


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['laundry_shop', 'paws']


class ServicePriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['laundry_shop', 'service', 'price']

class LaundryShopForm(forms.ModelForm):
    class Meta:
        model = LaundryShop
        fields = ['barangay', 'building', 'city', 'contact_number',
        'days_open', 'email', 'hours_open', 'name', 'province',
        'street', 'website']