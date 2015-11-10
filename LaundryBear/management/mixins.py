from LaundryBear.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class AdminLoginRequiredMixin(LoginRequiredMixin):
    login_view_name = 'management:login-admin'
