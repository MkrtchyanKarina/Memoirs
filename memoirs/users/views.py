from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView

from post.utils import DataMixin
from users.forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    extra_context = {'title': 'Авторизация'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')



