from django.core.urlresolvers import reverse
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView
from django.forms.models import inlineformset_factory

from database.models import LaundryShop, Service, Price

from management import forms


class LaundryMenuView(TemplateView):
    template_name = 'management/shop/laundrybearmenu.html'

    def get_context_data(self, **kwargs):
        context = super(LaundryMenuView, self).get_context_data(**kwargs)
        context['recent_shops'] = LaundryShop.objects.order_by(
            '-creation_date')[:3]
        return context


class LaundryUpdateView(UpdateView):
    template_name = 'management/shop/editlaundryshop.html'
    model = LaundryShop
    form_class = forms.LaundryShopForm

    def get_success_url(self):
        return reverse('management:list-shops')


class LaundryCreateView(CreateView):
    template_name = 'management/shop/addlaundryshop.html'
    model = LaundryShop
    form_class = forms.LaundryShopForm

    def get_success_url(self):
        return reverse('management:list-shops')

    def form_valid(self, form):
        response = super(LaundryCreateView, self).form_valid(form)
        PriceInlineFormSet = inlineformset_factory(
            LaundryShop, Price, fields=('service', 'price'), extra=1)
        price_formset = PriceInlineFormSet(
            data=self.request.POST, instance=self.object)
        if price_formset.is_valid():
            price_formset.save()
        else:
            print price_formset.errors
        return response

    def get_context_data(self,**kwargs):
        context = super(LaundryCreateView, self).get_context_data(**kwargs)
        context['service_list'] = Service.objects.all()
        price_formset = inlineformset_factory(
            LaundryShop, Price, fields=('service', 'price'), extra=1)
        context['price_formset'] = price_formset()
        return context

    def post(self, request, *args, **kwargs):
        response = super(LaundryCreateView, self).post(request, *args, **kwargs)
        price_form = forms.ServicePriceForm(data=request.POST)
        if price_form.is_valid():
            price_form.save()
        else:
            print price_form.errors
        return response


class LaundryDeleteView(DeleteView):
    model = LaundryShop

    def get_success_url(self):
        return reverse('management:list-shops')

class LaundryListView(ListView):
    model = LaundryShop
    paginate_by = 10
    template_name = 'management/shop/viewlaundryshops.html'
    context_object_name = 'shop_list'

    def get_context_data(self, **kwargs):
        context = super(LaundryListView, self).get_context_data(**kwargs)
        shops = context['shop_list']
        name_query = self.request.GET.get('name', False)
        query_type = 'name'
        if name_query:
            shops = self.get_shops_by_name(name_query)
            query_type = 'name'
        city_query = self.request.GET.get('city', False)
        if city_query:
            shops = self.get_shops_by_city(city_query)
            query_type = 'city'
        province_query = self.request.GET.get('province', False)
        if province_query:
            shops = self.get_shops_by_province(province_query)
            query_type = 'province'
        barangay_query = self.request.GET.get('barangay', False)
        if barangay_query:
            shops = self.get_shops_by_barangay(barangay_query)
            query_type = 'barangay'
        context.update({'shop_list': shops})
        context['query_type'] = query_type
        return context

    def get_shops_by_name(self, name_query):
        return LaundryShop.objects.filter(name__icontains=name_query)

    def get_shops_by_city(self, city_query):
        return LaundryShop.objects.filter(city__icontains=city_query)

    def get_shops_by_province(self, province_query):
        return LaundryShop.objects.filter(province__icontains=province_query)

    def get_shops_by_barangay(self, barangay_query):
        return LaundryShop.objects.filter(barangay__icontains=barangay_query)
