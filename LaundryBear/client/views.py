from django.shortcuts import render

# Create your views here.

class ClientLoginView(TemplateView):
    template_name = "client/account/login.html"

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_authenticated():
            return redirect('management:menu')
        return render(self.request, self.template_name, {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('client:success')
            else:
                return render(request, self.template_name, {})
        else:
            return render(request, self.template_name, {})


class ClientLogoutView(RedirectView):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('client:success')

class SuccessView(TemplateView):
    template_name = "client/success.html"
