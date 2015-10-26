from django.shortcuts import render
from django.core.urlresolvers import reverse
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
    fields = ['name','building','street','barangay','city','province'
        'contact_number','website','email','hours_open','days_open']


class LaundryCreateView(CreateView):
    template_name = 'management/shop/addlaundryshop.html'
    model = LaundryShop
    fields = ['barangay', 'building', 'city', 'contact_number',
        'days_open', 'email', 'hours_open', 'name', 'province',
        'street', 'website']

    def get_success_url(self):
        return reverse('management:list-shops')

    def form_valid(self, form):
        response = super(LaundryCreateView, self).form_valid(form)
        post_data = self.request.POST.copy()
        post_data.update({'laundry_shop': self.object.pk})
        rating_form = forms.RatingForm(data=post_data)
        if rating_form.is_valid():
            rating_form.save()
        return response


class LaundryListView(ListView):
    model = LaundryShop
    paginate_by = 10
    template_name = 'management/shop/viewlaundryshops.html'
    context_object_name = 'shop_list'

    def get_context_data(self, **kwargs):
        context = super(LaundryListView, self).get_context_data(**kwargs)
        shops = context['shop_list']
        name_query = self.request.GET.get('name', False)
        if name_query:
            shops = self.get_shops_by_name(name_query)
        city_query = self.request.GET.get('city', False)
        if city_query:
            shops = self.get_shops_by_city(city_query)
        province_query = self.request.GET.get('province', False)
        if province_query:
            shops = self.get_shops_by_province(province_query)
        context.update({'shop_list': shops})
        return context

    def get_shops_by_name(self, name_query):
        return LaundryShop.objects.filter(name__icontains = name_query)

    def get_shops_by_city(self, city_query):
        return LaundryShop.objects.filter(city__icontains = city_query)

    def get_shops_by_province(self, province_query):
        return LaundryShop.objects.filter(province__icontains = province_query)