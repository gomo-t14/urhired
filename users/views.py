from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import RegisterForm







# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'users/home.html'

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

#add profile view later





    