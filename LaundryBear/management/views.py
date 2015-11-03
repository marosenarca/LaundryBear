from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render
from django.views.generic import (CreateView, DeleteView, ListView,
    RedirectView, TemplateView, UpdateView)
from django.utils.decorators import method_decorator

from database.models import LaundryShop, Price, Service, UserProfile

from management import forms
from LaundryBear.mixins import LoginRequiredMixin

class LaundryMenuView(LoginRequiredMixin, TemplateView):
    template_name = 'management/shop/laundrybearmenu.html'

    def get_context_data(self, **kwargs):
        context = super(LaundryMenuView, self).get_context_data(**kwargs)
        context['recent_shops'] = LaundryShop.objects.order_by(
            '-creation_date')[:3]
        return context


class LaundryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'management/shop/editlaundryshop.html'
    model = LaundryShop
    form_class = forms.LaundryShopForm

    def get_success_url(self):
        return reverse('management:list-shops')

    def get_context_data(self,**kwargs):
        context = super(LaundryUpdateView, self).get_context_data(**kwargs)
        context['service_list'] = Service.objects.all().order_by('pk')
        price_formset = inlineformset_factory(
            LaundryShop, Price, fields=('service', 'price'), extra=1)
        context['price_formset'] = price_formset(instance=self.object)
        return context

class LaundryCreateView(LoginRequiredMixin, CreateView):
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
        context['service_list'] = Service.objects.all().order_by('pk')
        price_formset = inlineformset_factory(
            LaundryShop, Price, fields=('service', 'price'), extra=1)
        context['price_formset'] = price_formset()
        return context


class LaundryDeleteView(LoginRequiredMixin, DeleteView):
    model = LaundryShop

    def get_success_url(self):
        return reverse('management:list-shops')

class LaundryListView(LoginRequiredMixin, ListView):
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


class LoginView(TemplateView):
    template_name = "management/account/login.html"

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_authenticated():
            return redirect('management:menu')
        return render(self.request, self.template_name, {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active and user.is_staff:
                login(request, user)
                return redirect('management:menu')
            else:
                return redirect('client:menu')
        else:
            return render(request, self.template_name, {})


class LogoutView(RedirectView):
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_staff:
            logout(request)
            return redirect('management:login-admin')
        return redirect('management:menu')


class ClientListView(LoginRequiredMixin, ListView):
    model = UserProfile
    paginate_by = 10
    template_name = 'management/client/viewclients.html'
    context_object_name = 'client_list'

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        client = context['client_list']

        name_query = self.request.GET.get('name', False)
        query_type = 'name'
        if name_query:
            client = self.get_user_by_name(name_query)
            query_type = 'name'
        city_query = self.request.GET.get('city', False)
        if city_query:
            client = self.get_user_by_city(city_query)
            query_type = 'city'
        province_query = self.request.GET.get('province', False)
        if province_query:
            client = self.get_user_by_province(province_query)
            query_type = 'province'
        barangay_query = self.request.GET.get('barangay', False)
        if barangay_query:
            client = self.get_user_by_barangay(barangay_query)
            query_type = 'barangay'
        context.update({'client_list': client})
        context['query_type'] = query_type
        return context

    def get_user_by_name(self, name_query):
        return UserProfile.objects.filter(Q(client__first_name__icontains=name_query)|
            Q(client__last_name__icontains=name_query))

    def get_user_by_city(self, city_query):
        return UserProfile.objects.filter(city__icontains=city_query)

    def get_user_by_province(self, province_query):
        return UserProfile.objects.filter(province__icontains=province_query)

    def get_user_by_barangay(self, barangay_query):
        return UserProfile.objects.filter(barangay__icontains=barangay_query)

class ServicesListView(LoginRequiredMixin, ListView):
    model = Service
    paginate_by = 10
    template_name = 'management/shop/viewservices.html'
    context_object_name = 'service_list'

    def get_context_data(self, **kwargs):
        context = super(ServicesListView, self).get_context_data(**kwargs)
        service = context['service_list']

        name_query = self.request.GET.get('name', False)
        query_type = 'name'
        if name_query:
            service = self.get_user_by_name(name_query)
            query_type = 'name'
        description_query = self.request.GET.get('description', False)
        if description_query:
            service = self.get_user_by_city(description_query)
            query_type = 'description'

        context.update({'service_list': service})
        context['query_type'] = query_type
        return context

    def get_user_by_name(self, name_query):
        return Service.objects.filter(name__icontains=name_query)

    def get_user_by_city(self, description_query):
        return UserProfile.objects.filter(description__icontains=city_query)

class ServicesDeleteView(LoginRequiredMixin, DeleteView):
    model = Service

    def get_success_url(self):
        return reverse('management:list-service')       
