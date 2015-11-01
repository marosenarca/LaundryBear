from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, ListView,
    RedirectView, TemplateView, UpdateView)

from client.forms import ProfileForm, UserForm
from database.models import UserProfile
from LaundryBear.mixins import LoginRequiredMixin
# Create your views here.

class ClientLoginView(TemplateView):
    template_name = "client/usersignin.html"

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_authenticated():
            return render(self.request, DashView.template_name, {})
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


class DashView(LoginRequiredMixin, TemplateView):
    template_name = "client/success.html"

    def get(self, request):
        if request.user.is_authenticated():
            return render(request, self.template_name, {})
        return redirect('client:login')

class SignupView(CreateView):
    template_name = "client/signup.html"
    model = UserProfile
    form_class = UserCreationForm
    upf = ProfileForm

    def get_success_url(self):
        return reverse('client:menu')

    def form_valid(self, form):
        response = super(SignupView, self).form_valid(form)

        #if self.form_class.is_valid():
        #    user = self.form_class.save()
        user = SignupView.form_class
        userprofile = SignupView.upf.save(commit=False)
        userprofile.user = user
        print 'uf is valid'
        if upf.is_valid():
            print 'upf is valid'
            print userprofile.user
            print '----------'
            print user
            print 'teee'
            userprofile.save()
        else:
            print upf.errors
        print '=================='
        print uf.errors
        print '------------------'
        print upf.errors
        print '=================='
        return response

    def get_success_url(self):
        return reverse('client:menu')

    def get(self, request):
        uf = self.form_class
        upf = self.upf
        return render_to_response(self.template_name,
                                               dict(userform=uf,
                                                    userprofileform=upf),
                                               context_instance=RequestContext(request))
