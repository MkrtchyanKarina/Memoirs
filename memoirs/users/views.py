from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, DetailView

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



class ChangeUserInformation(LoginRequiredMixin, UpdateView):
    """ Обновление информации о пользователе """
    model = get_user_model()
    pk_url_kwarg = "user_id"
    template_name = "users/register.html"
    extra_context = {'title': 'Изменение информации'}
    fields = ['username', 'email', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse('users:info', kwargs={'user_id': self.object.pk})

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if user.pk != request.user.pk:
            messages.error(request, "У вас нет прав на редактирование информации об этом пользователе!")
            return redirect('home_page')
        else:
            return super().get(request, *args, **kwargs)




class ShowUserInformation(LoginRequiredMixin, DetailView):
    """ Информация о текущем пользователе """
    model = get_user_model()
    pk_url_kwarg = "user_id"
    template_name = "users/info.html"
    context_object_name = 'user'
    extra_context = {'title': 'Информация'}

    def get_success_url(self):
        return reverse('users:info', kwargs={'user_id': self.object.pk})

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if user.pk != request.user.pk:
            messages.error(request, "У вас нет прав на просмотр информации об этом пользователе!")
            return redirect('home_page')
        return super().get(request, *args, *kwargs)








