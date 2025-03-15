from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_list_or_404, render, get_object_or_404
from .models import Post, Category, TagPost


menu = [
    {'title': "Главная страница", 'url_name': 'home_page'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить пост", 'url_name': 'add_post'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Post.published.filter(cat_id=category.pk)
    data = {
        'title': f'Категория: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,

    }
    return render(request, 'post/index.html', context=data)


def index(request):
    data = {
        'title': 'home page',
        'menu': menu,
        'posts': Post.published.all(),
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
    post = Post.published.get(pk=post_id)
    data = {
        'menu': menu,
        'post': post,
        'cat_selected': post.cat_id,
    }
    return render(request, 'post/post.html', context=data)


def show_tag_posts_list(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Post.Status.PUBLISHED)

    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'post/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
