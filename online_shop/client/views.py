from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def client_signup(request):
    if request.method == 'POST':
        client_form = UserRegisterForm(request.POST)
        if client_form.is_valid():
            client_form.save()
            username = client_form.cleaned_data.get('username')
            email = client_form.cleaned_data.get('email')
            # messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('client_login')
        else:
            print("Sign up cannot be performed")
    else:
        client_form = UserRegisterForm()
    context = {
        'client_form': client_form
    }
    return render(request, 'client/signup.html', context)


def client_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            # messages.success(request, f' welcome {username} !!')
            return redirect('home')
        else:
            print("Login cannot be performed")
            # messages.info(request, f'account done not exit plz sign in')
    context = {
        'client_form': AuthenticationForm()
    }
    return render(request, 'client/login.html', context)
