from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # Авторизация и выход из аккаунта
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home_page'), name='logout'),

    # Регистрация
    path('register/', views.RegisterUser.as_view(), name='register'),

    # Личный кабинет пользователя: изменение информации, посты, комментарии
    path('edit/<int:user_id>/', views.EditUserInformation.as_view(), name='edit'),
    path('profile/<int:user_id>/', views.ShowPersonalInformation.as_view(), name='profile'),
    path('comments/', views.UsersCommentsList.as_view(), name='comments'),

    # Смена пароля
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
]