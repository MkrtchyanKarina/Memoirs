from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_list_or_404, render, get_object_or_404
from .models import Post


menu = [
    {'title': "Главная страница", 'url_name': 'home_page'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить пост", 'url_name': 'add_post'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]

categories_db = [
    # {'id': 1, 'name': 'Новости'},
    {'id': 2, 'name': 'Обзоры'},
    {'id': 3, 'name': 'Тренды'},
    {'id': 3, 'name': 'Исследования'},
    # {'id': 3, 'name': 'Без категории'},
    {'id': 3, 'name': 'Советы'},
    {'id': 3, 'name': 'Интервью'},
    {'id': 3, 'name': 'Личный опыт'},
]

"""
    {'id': 1, 'name': 'Личный опыт'},
    {'id': 2, 'name': 'Здоровье'},
    Автомобили
    {'id': 3, 'name': 'Путешествия'},
    {'id': 4, 'name': 'Кулинария'},
    {'id': 5, 'name': 'Технологии'},
    {'id': 6, 'name': 'Хобби'},
    {'id': 7, 'name': 'Искусство'},
    {'id': 8, 'name': 'Литература'},
    {'id': 8, 'name': 'Архитектура'},
    {'id': 8, 'name': 'Биография'},
    {'id': 8, 'name': 'Наука'},
    {'id': 8, 'name': 'Кино'},
    {'id': 9, 'name': 'Театр'},
    {'id': 10, 'name': 'Музыка'},
    {'id': 11, 'name': 'Мода'},
"""

def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': get_list_or_404(Post, is_published=1),
        'cat_selected': cat_id,

    }
    return render(request, 'post/index.html', context=data)


def index(request):
    data = {
        'title': 'home page',
        'menu': menu,
        'posts': Post.published.all(),
        # 'posts': get_list_or_404(Post, is_published=1),
        'cat_selected': 0,
        }
    return render(request, 'post/index.html', context=data)


def about(request):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'post/about.html', context=data)


def add_post(request):
    return HttpResponse("<h1>Добавление нового поста в блог</h1>")


def login(request):
    return HttpResponse("<h1>Войти или зарегистрироваться</h1>")


def contact(request):
    return HttpResponse("<h1>Обратная связь</h1>")


def show_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    data = {
        'menu': menu,
        'post': post,
        'cat_selected': 2,
    }
    return render(request, 'post/post.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
