from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm
from .models import Post, TagPost
from .utils import DataMixin



class PostHome(DataMixin, ListView):
    """
    Представление для отображения главной страницы с опубликованными постами.

    Атрибуты:
        :template_name (str): Путь к шаблону, который будет использоваться для отображения страницы.
        :context_object_name (str): Имя переменной контекста, в которой будут храниться объекты.
        :title (str): Заголовок страницы.
        :cat_selected (int): Идентификатор выбранной категории (по умолчанию 0).
    """
    template_name = "post/index.html"
    context_object_name = 'posts'
    title = 'Главная страница'
    cat_selected = 0


    def get_queryset(self):
        """
        Возвращает список опубликованных постов.

        Использует метод select_related для предварительной выборки связанных
        объектов категорий, что позволяет уменьшить количество запросов к базе данных.
        """
        return Post.published.all().select_related('cat')



def about(request):
    contact_list = Post.published.all()
    paginator = Paginator(contact_list, 3)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)


    return render(request, 'post/about.html', context={'page_obj': page_obj, 'title': 'О сайте'})



class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'post/add_post.html'
    extra_context = {'title': 'Добавление статьи'}

    def form_valid(self, form):
        """ Функция сохранения формы после получения данных о текущем пользователе """
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, DataMixin, UpdateView):
    model = Post
    form_class = AddPostForm
    template_name = 'post/add_post.html'
    title = 'Обновление статьи'

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            messages.error(request, "У вас нет прав на редактирование этого поста!")
            return redirect('home_page')
        else:
            return super().get(request, *args, **kwargs)



class DeletePost(LoginRequiredMixin, DataMixin, DeleteView):
    model = Post
    template_name = 'post/add_post.html'
    success_url = reverse_lazy('home_page')
    title = 'Удаление статьи'

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            messages.error(request, "У вас нет прав на удаление этого поста!")
            return redirect('home_page')
        else:
            return super().get(request, *args, **kwargs)


class UsersPostsList(DataMixin, ListView):
    model = Post
    template_name = 'post/index.html'
    context_object_name = 'posts'
    cat_selected = 0
    title = 'Ваши посты'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('users:login'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update(self.get_mixin_context(
    #         title=self.title,
    #         cat_selected=self.cat_selected
    #     ))
    #     return context

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
