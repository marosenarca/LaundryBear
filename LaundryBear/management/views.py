from django.shortcuts import render
from django.views.generic import UpdateView, TemplateView

from database.models import LaundryShop


class LaundryMenuView(TemplateView):
    template_name = 'management/shop/laundrybearmenu.html'


class LaundryUpdateView(UpdateView):
    template_name = 'management/shop/editlaundryshop.html'
    model = LaundryShop
