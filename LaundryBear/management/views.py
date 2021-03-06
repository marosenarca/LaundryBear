import json

from database.models import LaundryShop, Price, Service, UserProfile, Transaction, Order, Fees

from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, FormView, ListView,
    RedirectView, TemplateView, UpdateView)

from management import forms
from management.mixins import AdminLoginRequiredMixin

from LaundryBear.views import LoginView, LogoutView
from django.contrib.auth.forms import PasswordChangeForm

#Django uses class based views to connect with templates.
#Each class based view has their own methods.
#You can still add more methods if needed.
#Check ccbv.co.uk for more information

class LaundryMenuView(AdminLoginRequiredMixin, TemplateView):
    template_name = 'management/shop/laundrybearmenu.html'

    def get_context_data(self, **kwargs):
        context = super(LaundryMenuView, self).get_context_data(**kwargs)
        context['recent_shops'] = LaundryShop.objects.order_by(
            '-creation_date')[:3]
        return context


class LaundryUpdateView(AdminLoginRequiredMixin, UpdateView):
    template_name = 'management/shop/editlaundryshop.html'
    model = LaundryShop
    form_class = forms.LaundryShopForm

    def get_success_url(self):
        return reverse('management:list-shops')

    def form_valid(self, form):
        response = super(LaundryUpdateView, self).form_valid(form)
        PriceInlineFormSet = inlineformset_factory(
            LaundryShop, Price, fields=('service', 'price', 'duration'), extra=1)
        price_formset = PriceInlineFormSet(
            data=self.request.POST, instance=self.object)
        if price_formset.is_valid():
            price_formset.save()
        else:
            print price_formset.errors
        return response

    def get_context_data(self,**kwargs):
        context = super(LaundryUpdateView, self).get_context_data(**kwargs)
        context['service_list'] = Service.objects.all().order_by('pk')
        price_formset = inlineformset_factory(
            LaundryShop, Price, fields=('service', 'price', 'duration'), extra=1)
        context['price_formset'] = price_formset(instance=self.object)
        return context

class LaundryCreateView(AdminLoginRequiredMixin, CreateView):
    template_name = 'management/shop/addlaundryshop.html'
    model = LaundryShop
    form_class = forms.LaundryShopForm

    def get_success_url(self):
        return reverse('management:list-shops')

    def form_valid(self, form):
        response = super(LaundryCreateView, self).form_valid(form)
        PriceInlineFormSet = inlineformset_factory(
            LaundryShop, Price, fields=('service', 'price', 'duration'), extra=1)
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
            LaundryShop, Price, fields=('service', 'price', 'duration'), extra=1)
        context['price_formset'] = price_formset()
        return context


class LaundryDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = LaundryShop

    def get_success_url(self):
        return reverse('management:list-shops')

class LaundryListView(AdminLoginRequiredMixin, ListView):
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


class AdminLoginView(LoginView):
    template_name = "management/account/login.html"
    form_class = forms.AdminLoginForm
    success_view_name = 'management:menu'


class AdminLogoutView(LogoutView):
    login_view_name = 'management:login-admin'


class ClientListView(AdminLoginRequiredMixin, ListView):
    model = UserProfile
    paginate_by = 10
    template_name = 'management/client/viewclients.html'
    context_object_name = 'client_list'
    ordering = ['client__first_name', 'client__last_name']

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


class ServicesListView(AdminLoginRequiredMixin, ListView):
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
            service = self.get_service_by_name(name_query)
            query_type = 'name'
        description_query = self.request.GET.get('description', False)
        if description_query:
            service = self.get_service_by_description(description_query)
            query_type = 'description'

        context.update({'service_list': service})
        context['query_type'] = query_type
        return context

    def get_service_by_name(self, name_query):
        return Service.objects.filter(name__icontains=name_query)

    def get_service_by_description(self, description_query):
        return Service.objects.filter(description__icontains=description_query)

class ServicesDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = Service

    def get_success_url(self):
        return reverse('management:list-service')


class ServiceCreateView(AdminLoginRequiredMixin, CreateView):
    template_name = 'management/shop/partials/createservice.html'
    model = Service
    form_class = forms.ServiceForm

    def post(self, request, *args, **kwargs):
        response = super(ServiceCreateView, self).post(request, *args, **kwargs)
        if self.object:
            service = {}
            service['name'] = self.object.name
            service['description'] = self.object.description
            service['pk'] = self.object.pk
            return HttpResponse(json.dumps(service))
        else:
            return response

    def get_success_url(self):
        return reverse('management:create-service')


class ServiceUpdateView(AdminLoginRequiredMixin, UpdateView):
    template_name = 'management/shop/editservices.html'
    model = Service
    form_class = forms.ServiceForm

    def get_success_url(self):
        return reverse('management:list-service')


class AddNewServiceView(AdminLoginRequiredMixin, CreateView):
    template_name = 'management/shop/addnewservice.html'
    model = Service
    form_class = forms.ServiceForm

    def get_success_url(self):
        return reverse('management:list-service')


class PendingRequestedTransactionsView(AdminLoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'pending_transaction_list'
    template_name = 'management/transactions/pending_requested_transactions.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super(PendingRequestedTransactionsView, self).get_queryset()
        queryset = queryset.filter(status=1)

        return queryset


class OngoingTransactionsView(AdminLoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'ongoing_transaction_list'
    template_name = 'management/transactions/ongoing_transactions.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(OngoingTransactionsView,self).get_context_data(**kwargs)
        form_list = []
        for transaction in self.object_list:
            form_list.append(forms.TransactionPriceForm(prefix=transaction.pk, data=self.request.POST or None, instance=transaction))

        context['transaction_list'] = zip(self.object_list, form_list)
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        form_list = context['transaction_list']
        for transaction, form in form_list:
            if form.is_valid():
                form.save()

        return redirect('management:ongoing-transactions')


    def get_queryset(self):
        queryset = super(OngoingTransactionsView, self).get_queryset()
        queryset = queryset.filter(status=2)

        return queryset


class HistoryTransactionsView(AdminLoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'history_transaction_list'
    template_name = 'management/transactions/history_transactions.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super(HistoryTransactionsView, self).get_queryset()
        filters = (3,4)
        queryset = queryset.filter(status__in=filters).order_by('request_date').reverse()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(HistoryTransactionsView, self).get_context_data(**kwargs)
        transaction = context['history_transaction_list']

        name_query = self.request.GET.get('client name', False)
        query_type = 'client name'
        if name_query:
            transaction = self.get_transaction_by_name(name_query)
            query_type = 'client name'

        shop_query = self.request.GET.get('laundry shop', False)
        if shop_query:
            transaction = self.get_transaction_by_shop(shop_query)
            query_type = 'laundry shop'

        context.update({'history_transaction_list': transaction})
        context['query_type'] = query_type
        return context

    def get_transaction_by_name(self, name_query):
        return Transaction.objects.filter(Q(client__client__first_name__icontains=name_query)|
            Q(client__client__last_name__icontains=name_query))

    def get_transaction_by_shop(self, shop_query):
        return Transaction.objects.filter(order__price__laundry_shop__name__icontains=shop_query)



class UpdateTransactionDeliveryDateView(AdminLoginRequiredMixin, UpdateView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'management/transactions/update_transaction.html'
    fields = ['delivery_date']

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateTransactionDeliveryDateView, self)\
            .get_context_data(*args, **kwargs)
        context['fees'] = Site.objects.get_current().fees
        return context

    def get_success_url(self):
        return reverse('management:pending-transactions')

    def post(self, request, *args, **kwargs):
        response = super(UpdateTransactionDeliveryDateView, self).post(request, *args, **kwargs)
        if request.POST.get('approve', False):
            self.object.status = 2
            self.object.save()
        else:
            self.object.status = 4
            self.object.save()
        return response


class MarkTransactionDoneView(AdminLoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ['status']
    template_name = ''

    def get_success_url(self):
        return reverse('management:ongoing-transactions')

class AdminSettingsView(AdminLoginRequiredMixin, TemplateView):
    template_name = 'management/account/settings.html'

    def get_context_data(self, **kwargs):
        context = super(AdminSettingsView, self).get_context_data(**kwargs)
        context['usernameform'] = forms.ChangeUsernameForm(data=self.request.POST or None, instance=self.request.user)
        context['passwordform'] = PasswordChangeForm(data=self.request.POST or None, user=self.request.user)
        site = Site.objects.get_current()
        context['fees_form'] = forms.FeesForm(data=self.request.POST or None,
            instance=site.fees)
        return context

    def post(self,request,*args,**kwargs):
        context = self.get_context_data(*args, **kwargs)
        usernameform = context['usernameform']
        passwordform = context['passwordform']

        if (usernameform.is_valid()):
            usernameform.save()
        else:
            print usernameform.errors

        if passwordform.is_valid():
            passwordform.save()
        else:
            print passwordform.error_messages

        fees_form = context['fees_form']
        if fees_form.is_valid():
            fees_form.save()
        return self.render_to_response(context)

