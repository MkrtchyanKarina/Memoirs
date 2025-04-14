from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from .forms import AddPostForm
from .models import Post, TagPost

menu = [
    {'title': "Главная страница", 'url_name': 'home_page'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить пост", 'url_name': 'add_post'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]


class PostCategory(ListView):
    template_name = 'post/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = f'Категория: {cat.name}'
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


class PostHome(ListView):
    template_name = "post/index.html"
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Post.published.all().select_related('cat')



def about(request):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'post/about.html', context=data)



class AddPost(FormView):
    form_class = AddPostForm
    template_name = 'post/add_post.html'
    success_url = reverse_lazy('home_page')
    extra_context = {
        'title': 'Добавление статьи',
        'menu': menu,
        'cat_selected': 0,
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



def login(request):
    return HttpResponse("<h1>Войти или зарегистрироваться</h1>")


def contact(request):
    return HttpResponse("<h1>Обратная связь</h1>")


class ShowPost(DetailView):
    template_name = 'post/post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['menu'] = menu
        context['cat_selected'] = context['post'].cat
        context['title'] = context['post'].title
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post.published, pk=self.kwargs['post_id'])


class TagPostList(ListView):
    context_object_name = 'posts'
    template_name = 'post/index.html'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context = super().get_context_data(**kwargs)
        context['title'] = f'Тег: {tag.tag}'
        context['menu'] = menu
        context['cat_selected'] = None
        return context


def page_not_found(request, exception):
    """
    Страница, которая будет отображаться при ошибке 404 в режиме DEBUG=False
    :param request: информация о текущем http-запросе
    :param exception: информация об ошибке
    :return: сообщение "Страница не найдена"
    """
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
