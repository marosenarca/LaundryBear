from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.LaundryMenuView.as_view(), name='menu'),
    url(r'^shops/add$', views.LaundryCreateView.as_view(), name='add-shop'),
    url(r'^shops/edit/(?P<pk>\d+)$', views.LaundryUpdateView.as_view(),
        name='edit-shop'),
    url(r'^shops/list$', views.LaundryListView.as_view(), name='list-shops'),
    url(r'^shops/delete/(?P<pk>\d+)$', views.LaundryDeleteView.as_view(), name='delete-shop')
]
