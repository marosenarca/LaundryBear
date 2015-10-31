from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render
from django.views.generic import (CreateView, DeleteView, ListView,
    RedirectView, TemplateView, UpdateView)
from django.utils.decorators import method_decorator

from LaundryBear.mixins import LoginRequiredMixin
# Create your views here.

class ClientLoginView(TemplateView):
    template_name = "client/usersignin.html"

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_authenticated():
            return render(self.request, SuccessView.template_name, {})
        return render(self.request, self.template_name, {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('client:menu')
            else:
                return render(request, self.template_name, {})
        else:
            return render(request, self.template_name, {})


class ClientLogoutView(RedirectView):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        print 'logged out'
        return redirect('client:login')


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "client/success.html"
