from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = [
    url(r'^login', views.ClientLoginView.as_view(), name='login'),
    url(r'^logout', views.ClientLogoutView.as_view(), name='logout'),
    url(r'', views.DashView.as_view(), name='menu')
]
