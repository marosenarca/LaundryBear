from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, TemplateView

from database.models import LaundryShop, Service

from management import forms


class LaundryMenuView(TemplateView):
    template_name = 'management/shop/laundrybearmenu.html'

    def get_context_data(self, **kwargs):
        context = super(LaundryMenuView, self).get_context_data(**kwargs)
        context['recent_shops'] = LaundryShop.objects.order_by('-creation_date')[:3]
        return context


class LaundryUpdateView(UpdateView):
    template_name = 'management/shop/editlaundryshop.html'
    model = LaundryShop
    fields = ['name',]


class LaundryCreateView(CreateView):
    template_name = 'management/shop/addlaundryshop.html'
    model = LaundryShop
    fields = ['barangay', 'building', 'city', 'contact_number',
        'days_open', 'email', 'hours_open', 'name', 'province',
        'street', 'website']


class ServiceCreateView(CreateView):
    template_name = 'management/shop/addservice.html'
    model = Service
    form_class = forms.ServiceForm

class LaundryListView(CreateView):
    template_name = 'management/shop/viewlaundryshops.html'
    model = Service
    form_class = forms.ServiceForm
