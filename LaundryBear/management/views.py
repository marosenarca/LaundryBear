from django.shortcuts import render
from django.views.generic import CreateView, TemplateView

from database.models import LaundryShop


class LaundryMenuView(TemplateView):
    template_name = 'management/shop/laundrybearmenu.html'


class LaundryCreateView(CreateView):
    template_name = 'management/shop/addlaundryshop.html'
    form_class = None
    model = LaundryShop
    fields = ['name', 'province', 'city', 'barangay', 'street', 'building', 'contact_number', 'email', 'website', 'hours_open', 'days_open']

