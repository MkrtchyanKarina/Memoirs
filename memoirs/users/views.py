from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from users.forms import LoginUserForm


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    extra_context = {'title': 'Авторизация'}


    # def get_success_url(self):
    #     return reverse_lazy("home_page")

# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))
