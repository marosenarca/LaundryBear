from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = [
    url(r'^login', views.ClientLoginView.as_view(), name='login'),
    url(r'^logout', views.ClientLogoutView.as_view(), name='logout'),
    url(r'^signup', views.SignupView.as_view(), name='signup'),
    url(r'^viewshops', views.ShopsListView.as_view(), name='view-shops'),
    url(r'^order/(?P<pk>\d+)$', views.OrderView.as_view(), name='order'),
    url(r'^order/(?P<pk>\d+)/ordersummary$', views.OrderSummaryView.as_view(), name='order-summary'),
    url(r'', views.DashView.as_view(), name='menu')
]
