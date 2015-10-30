from django.conf.urls import include, url
from django.core.urlresolvers import reverse

from . import views


urlpatterns = [
    url(r'^$', views.LaundryMenuView.as_view(), name='menu'),
    url(r'^shops/add$', views.LaundryCreateView.as_view(), name='add-shop'),
    url(r'^shops/edit/(?P<pk>\d+)$', views.LaundryUpdateView.as_view(),
        name='edit-shop'),
    url(r'^shops/list$', views.LaundryListView.as_view(), name='list-shops'),
    url(r'^shops/delete/(?P<pk>\d+)$', views.LaundryDeleteView.as_view(), name='delete-shop'),
    url(r'^login', views.LoginView.as_view(), name='login-admin')
    #url(r'^login$', auth_views.login, {'template_name':'management/account/login.html', 'current_app':'management'}, name='login-admin'),
    #url(r'^logout$', auth_views.logout_then_login, {'login_url':'/management/login'}, name='logout-admin')
    #url(r'^login$', include('django.contrib.auth.urls', namespace='auth'))
]
