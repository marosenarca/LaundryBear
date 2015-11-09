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
        return redirect('client:login')


class DashView(LoginRequiredMixin, TemplateView):
    template_name = "client/success.html"

    def get(self, request):
        if request.user.is_authenticated():
            return render(request, self.template_name, {})
        return redirect('client:login')


class SignupView(TemplateView):
    template_name = "client/signup.html"

    def get_success_url(self):
        return reverse('client:menu')

    def post(self, request):
        uf = UserForm(request.POST, prefix='user')
        upf = ProfileForm(request.POST, prefix='userprofile')
        # Note: in the ProfileForm do not include the user
        if uf.is_valid() and upf.is_valid(): # check if both forms are valid
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.client= user
            userprofile.save()
            username = userprofile.client.username
            password = request.POST['user-password1']
            user = authenticate(username=username, password=password)
            login(request, user)    
            return redirect('client:menu')
        else:
            print uf.errors
            print upf.errors
            return self.render_to_response({'userform': uf, 'userprofileform': upf, 'view': self})


    def get(self, request):
        uf = UserForm(prefix='user')
        upf = ProfileForm(prefix='userprofile')
        return render_to_response(SignupView.template_name,
                                               dict(userform=uf,
                                                    userprofileform=upf),
                                               context_instance=RequestContext(request))

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(request=self.request, template=self.template_name, context=context, using=None, **response_kwargs)
