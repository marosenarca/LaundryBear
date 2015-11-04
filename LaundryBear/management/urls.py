from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()

from . import views


urlpatterns = [
    url(r'^menu$', views.LaundryMenuView.as_view(), name='menu'),
    url(r'^shops/add$', views.LaundryCreateView.as_view(), name='add-shop'),
    url(r'^shops/edit/(?P<pk>\d+)$', views.LaundryUpdateView.as_view(),
        name='edit-shop'),
    url(r'^shops/list$', views.LaundryListView.as_view(), name='list-shops'),
    url(r'^shops/delete/(?P<pk>\d+)$', views.LaundryDeleteView.as_view(),
        name='delete-shop'),
    url(r'^login$', views.LoginView.as_view(), name='login-admin'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout-admin'),
    url(r'^clients/list$', views.ClientListView.as_view(), name='list-client'),
    url(r'^services/list$', views.ServicesListView.as_view(),
        name='list-service'),
    url(r'^services/delete/(?P<pk>\d+)$', views.ServicesDeleteView.as_view(),
        name='delete-service'),
    url(r'^services/add$', views.ServiceCreateView.as_view(),
        name='create-service'),
    url(r'^services/edit/(?P<pk>\d+)$', views.ServiceUpdateView.as_view(),
        name='edit-service'),
    url(r'^service/add$', views.AddNewServiceView.as_view(), name='add-service')
]
