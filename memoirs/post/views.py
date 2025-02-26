from django.http import HttpResponse
from django.shortcuts import get_list_or_404, render
from .models import Post


menu = [
    {'title': "Главная страница", 'url_name': 'home_page'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить пост", 'url_name': 'add_post'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]



def index(request):
    data = {
        'title': 'home page',
        'menu': menu,
        }
    return render(request, 'post/index.html', context=data)


def about(request):
    return HttpResponse("<h1>Информация о сайте</h1>")
    # data = {'title': 'О сайте', 'menu': menu}
    # return render(request, 'posts/about.html', context=data)


def add_post(request):
    return HttpResponse("<h1>Добавление нового поста в блог</h1>")


def login(request):
    return HttpResponse("<h1>Войти или зарегистрироваться</h1>")


def contact(request):
    return HttpResponse("<h1>Обратная связь</h1>")


