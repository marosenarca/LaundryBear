from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from database.models import UserProfile


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'username', 'password']

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['client']
