import json

from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, FormView, ListView,
                                  RedirectView, TemplateView, UpdateView, View)

from client.forms import ProfileForm, UserForm
from client.mixins import ClientLoginRequiredMixin
from database.models import LaundryShop, Price, Service, UserProfile, Transaction, Order, default_date

from LaundryBear.forms import LoginForm
from LaundryBear.views import LoginView, LogoutView
# Create your views here.


class ClientLoginView(LoginView):
    template_name = "client/usersignin.html"
    form_class = LoginForm
    success_view_name = 'client:view-shops'


class ClientLogoutView(LogoutView):
    login_view_name = 'client:login'


class DashView(ClientLoginRequiredMixin, ListView):
    model = Transaction
    template_name = "client/dash.html"

    def get_context_data(self, **kwargs):
        context = super(DashView, self).get_context_data(**kwargs)
        context['transaction_list'] = self.get_transactions()
        return context


    def get_transactions(self):
        queryset = super(DashView, self).get_queryset()
        queryset = queryset.filter(client=self.request.user.userprofile)
        return queryset


class SignupView(TemplateView):
    template_name = "client/signup.html"

    def get_success_url(self):
        return reverse('client:menu')

    def post(self, request):
        uf = UserForm(request.POST, prefix='user')
        upf = ProfileForm(request.POST, prefix='userprofile')
        # Note: in the ProfileForm do not include the user
        if uf.is_valid() and upf.is_valid():  # check if both forms are valid
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.client = user
            userprofile.save()
            username = userprofile.client.username
            password = request.POST['user-password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('client:view-shops')
        else:
            print uf.errors
            print upf.errors
            return self.render_to_response({'userform': uf, 'userprofileform': upf, 'view': self})

    def get(self, request):
        uf = UserForm(prefix='user')
        upf = ProfileForm(prefix='userprofile')
        return render_to_response(SignupView.template_name,
                                  dict(userform=uf,
                                       userprofileform=upf),
                                  context_instance=RequestContext(request))

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(request=self.request, template=self.template_name, context=context, using=None, **response_kwargs)


class ShopsListView(ClientLoginRequiredMixin, ListView):
    model = LaundryShop
    paginate_by = 10
    template_name="client/viewshops.html"
    context_object_name = 'shop_list'

    def get_context_data(self, **kwargs):
        context = super(ShopsListView, self).get_context_data(**kwargs)
        shops = context['shop_list']

        query_type = ''

        name_query = self.request.GET.get('name', False)
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
        if barangay_query or not query_type:
            shops = self.get_shops_by_barangay(barangay_query or self.request.user.userprofile.barangay)
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


class OrderView(ClientLoginRequiredMixin, DetailView):
    context_object_name = 'shop'
    model = LaundryShop
    template_name="client/shopselect.html"

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        the_shop = context['shop']
        context['service_list'] = Price.objects.filter(laundry_shop__name=the_shop)
        return context


class OrderSummaryView(ClientLoginRequiredMixin, DetailView):
    context_object_name = 'shop'
    template_name="client/summaryoforder.html"
    model=LaundryShop

    def get_context_data(self, **kwargs):
        context = super(OrderSummaryView, self).get_context_data(**kwargs)
        context['delivery_fee'] = float(50)
        context['service_charge'] = float(50)
        context['delivery_date'] = default_date().strftime('%Y-%m-%d')
        context['delivery_date_max'] = (default_date() + timedelta(days=7)).strftime('%Y-%m-%d')
        return context


class CreateTransactionView(ClientLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=400)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            services = request.POST['selectedServices']
            services = json.loads(services)
            print request.POST
            transaction = Transaction.objects.create(client=request.user.userprofile, delivery_date=request.POST['delivery_date'])
            for service in services:
                pricePk = service['pk']
                price = Price.objects.get(pk=pricePk)
                Order.objects.create(price=price, pieces=service['pieces'], transaction=transaction)

            return HttpResponse(reverse('client:view-shops'))
        else:
            return HttpResponse(status=400)
