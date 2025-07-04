from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from users.forms import LoginUserForm, RegisterUserForm, EditUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    """ Отображение формы для входа в аккаунт """
    template_name = 'users/login.html'
    form_class = LoginUserForm
    extra_context = {'title': 'Авторизация'}



class RegisterUser(CreateView):
    """ Отображение страницы с формой для регистрации

    :success_url: если пользователь зарегистрировался, то перенаправляем на страницу входа в аккаунт 'users:login'
    """
    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')



class EditUserInformation(LoginRequiredMixin, UpdateView):
    """ Обновление информации о себе """
    model = get_user_model()
    form_class = EditUserForm
    pk_url_kwarg = "user_id"
    template_name = "users/edit_profile.html"
    extra_context = {'title': 'Изменение информации'}

    def get_success_url(self):
        return reverse('users:profile', kwargs={'user_id': self.object.pk})

    def get(self, request, *args, **kwargs):
        """
        Проверка прав пользователя

        :user: запрашиваемый пользователь
        :request.user: аутентифицированный пользователь
        """
        user = self.get_object()
        if user.pk != request.user.pk:
            messages.error(request, "У вас нет прав на редактирование информации об этом пользователе!")
            return redirect('home_page')
        else:
            return super().get(request, *args, **kwargs)


class UsersCommentsList(LoginRequiredMixin, ListView):
    """ Комментарии аутентифицированного пользователя """
    model = get_user_model()
    pk_url_kwarg = "user_id"
    template_name = "users/comments.html"
    context_object_name = 'comments'
    title = 'Комментарии пользователя'

    def get_queryset(self):
        """  Функция для получения списка комментариев аутентифицированного пользователя  """
        usr_id = self.request.user.pk
        return get_object_or_404(self.model, pk=usr_id).comments.all()




class ShowPersonalInformation(LoginRequiredMixin, DetailView):
    """ Информация о запрашиваемом пользователе """
    model = get_user_model()
    pk_url_kwarg = "user_id"
    template_name = "users/profile.html"
    context_object_name = 'user'
    extra_context = {'title': 'Информация'}


    def get_success_url(self):
        return reverse('users:profile', kwargs={'user_id': self.object.pk})


class UserPasswordChange(PasswordChangeView):
    """ Отображение формы для изменения пароля """
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    title = "Смена пароля"
