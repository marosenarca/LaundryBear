from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect

from LaundryBear import settings

#from management.views import LoginView

class LoginRequiredMixin(object):
    """
    View mixin which requires that the user is authenticated.
    """
    @method_decorator(user_passes_test(lambda u:u.is_staff, login_url='/client/login'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)
