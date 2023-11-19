from django import forms
from cosmetics.models import Client
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    address = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = Client
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'password1', 'password2']
