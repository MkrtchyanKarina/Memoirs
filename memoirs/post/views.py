from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm
from .models import Post, TagPost
from .utils import DataMixin



class PostHome(DataMixin, ListView):
    template_name = "post/index.html"
    context_object_name = 'posts'
    title = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Post.published.all().select_related('cat')



def about(request):
    data = {'title': 'О сайте'}
    return render(request, 'post/about.html', context=data)



class AddPost(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'post/add_post.html'
    title = 'Добавление статьи'


class UpdatePost(DataMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'images', 'is_published', 'cat', 'tags']
    template_name = 'post/add_post.html'
    success_url = reverse_lazy('home_page')
    title = 'Обновление статьи'


class DeletePost(DataMixin, DeleteView):
    model = Post
    template_name = 'post/add_post.html'
    success_url = reverse_lazy('home_page')
    title = 'Удаление статьи'



def login(request):
    return HttpResponse("<h1>Войти или зарегистрироваться</h1>")


def contact(request):
    return HttpResponse("<h1>Обратная связь</h1>")


class ShowPost(DataMixin, DetailView):
    template_name = 'post/post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title, cat_selected=context['post'].cat_id)


    def get_object(self, queryset=None):
        return get_object_or_404(Post.published, pk=self.kwargs['post_id'])


class PostCategory(DataMixin, ListView):
    template_name = 'post/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title=f"Категория: {cat.name}", cat_selected=cat.pk)


class TagPostList(DataMixin, ListView):
    context_object_name = 'posts'
    template_name = 'post/index.html'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title=f'Тег: {tag.tag}')



def page_not_found(request, exception):
    """
    Страница, которая будет отображаться при ошибке 404 в режиме DEBUG=False
    :param request: информация о текущем http-запросе
    :param exception: информация об ошибке
    :return: сообщение "Страница не найдена"
    """
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
