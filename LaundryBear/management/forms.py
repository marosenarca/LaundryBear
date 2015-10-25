from django import forms

from database.models import Rating, Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 5})}


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['laundry_shop', 'paws']
