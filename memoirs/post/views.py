from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_list_or_404, render, get_object_or_404, redirect

from .forms import AddPostForm
from .models import Post, Category, TagPost


menu = [
    {'title': "Главная страница", 'url_name': 'home_page'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить пост", 'url_name': 'add_post'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]


def show_category(request, cat_slug):
    """
    Функция отображения статей из выбранной категории на главной странице
    :param request: информация о текущем http-запросе
    :param cat_slug: выбранная категория (ее slug)
    :return: шаблон index.html - главная страница с боковым меню и списком статей из категории
    """
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Post.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Категория: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,

    }
    return render(request, 'post/index.html', context=data)


def index(request):
    """
    Функция для отображения главной страницы
    :param request: информация о текущем http-запросе
    :return: шаблон index.html - главная страница со всеми опубликованными записями, отсортированными от новых к старым
    """
    posts = Post.published.all().select_related('cat')
    data = {
        'title': 'home page',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
        }
    return render(request, 'post/index.html', context=data)


def about(request):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'post/about.html', context=data)


def add_post(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    else:
        form = AddPostForm()

    data = {
        'title': 'Добавить пост',
        'menu': menu,
        'form': form,
    }
    return render(request, 'post/add_post.html', context=data)


def login(request):
    return HttpResponse("<h1>Войти или зарегистрироваться</h1>")


def contact(request):
    return HttpResponse("<h1>Обратная связь</h1>")


def show_post(request, post_id):
    """
    Функция для отображения поста
    :param request: информация о текущем http-запросе
    :param post_id: идентификатор записи в БД
    :return: через шаблон post.html отображаются теги, связанные с этой записью, заголовок и содержимое
    """
    post = Post.published.get(pk=post_id)
    data = {
        'menu': menu,
        'post': post,
        'cat_selected': post.cat_id,
    }
    return render(request, 'post/post.html', context=data)


def show_tag_posts_list(request, tag_slug):
    """
    Функция отображения статей по выбранному тегу
    :param request: информация о текущем http-запросе
    :param tag_slug: выбранный тег (его slug)
    :return: шаблон index.html - главная страница с боковым меню и списком статей с искомым тегом
    """
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Post.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'post/index.html', context=data)


def page_not_found(request, exception):
    """
    Страница, которая будет отображаться при ошибке 404 в режиме DEBUG=False
    :param request: информация о текущем http-запросе
    :param exception: информация об ошибке
    :return: сообщение "Страница не найдена"
    """
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
