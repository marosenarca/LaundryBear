from django.contrib.auth.decorators import login_required
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
    #@method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return render(request, self.template_name, {})
        return redirect('%s?next=%s' % (settings.CLIENT_LOGIN_URL, request.path))
        #return super(LoginRequiredMixin, self).dispatch(
        #    request, *args, **kwargs)
        #return render(request, "base.html", {})
