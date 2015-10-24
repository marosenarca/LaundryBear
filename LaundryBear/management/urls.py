from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.LaundryMenuView.as_view(), name='menu'),
    url(r'^shops/add$', views.LaundryCreateView.as_view(), name='add-shop'),
    url(r'^shops/edit/(?P<pk>\d+)$', views.LaundryUpdateView.as_view(), name='edit-shop'),
    url(r'^shops/services/add$', views.ServiceCreateView.as_view(), name='add-service')
]
