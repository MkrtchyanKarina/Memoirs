from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    """  Менеджер для получения только опубликованных постов.  """

    def get_queryset(self):
        """  Возвращает queryset, содержащий только опубликованные посты.  """
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


class Post(models.Model):
    """
    Модель представления поста.

    Атрибуты:
        title (str): Заголовок поста.
        content (str): Содержимое поста.
        time_create (datetime): Время создания поста.
        time_update (datetime): Время последнего обновления поста.
        is_published (bool): Статус публикации поста (черновик или опубликован).
        cat (Category): Категория, к которой принадлежит пост.
        tags (TagPost): Теги, связанные с постом.
    """

    class Status(models.IntegerChoices):
        """  Статусы записи.  """
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="заголовок",
                             validators=[
                                 MinLengthValidator(5, message="Слишком короткий заголовок"),
                                 MaxLengthValidator(255, message="Слишком длинный заголовок")
                             ])
    content = models.TextField(blank=True, verbose_name="текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.PUBLISHED, verbose_name="статус")
    # преобразуем 1 и 0 в True и False для отображения выбранного виджета ("Опубликовано"/"Черновик") в админ-панели
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="posts", verbose_name="категории")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="теги")

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts', null=True, default=None)

    images = models.ImageField(upload_to="post_images/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Изображение")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        """  Возвращает строковое представление поста (его заголовок). """
        return self.title

    class Meta:
        """ Мета модель для изменения опций:
         verbose_name: для изменения названия модели при отображении в админ-панели
         ordering: сортировка статей от новых к старым (например, на главной странице или в списке статей конкретного пользователя)
         """
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        """   Возвращает URL для доступа к конкретному посту.   """
        return reverse('post', kwargs={'post_id': self.pk})


class Category(models.Model):
    """
    Модель для представления категории постов.

    Атрибуты:
        name (str): Название категории.
        slug (str): Уникальный слаг для категории.
    """

    objects = models.Manager()
    name = models.CharField(max_length=100, db_index=True, verbose_name="категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="слаг")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        """ Возвращает URL для доступа к конкретной категории. """
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        """  Возвращает строковое представление категории (ее название). """
        return self.name


class TagPost(models.Model):
    """
    Модель для представления тега поста.

    Атрибуты:
        tag (str): Название тега.
        slug (str): Уникальный слаг для тега.
    """
    objects = models.Manager()
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        """  Возвращает строковое представление тега (его название). """
        return self.tag

    def get_absolute_url(self):
        """ Возвращает URL для доступа к конкретному тегу. """
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Comment(models.Model):
    objects = models.Manager()
    text = models.TextField(blank=False, verbose_name='содержимое комментария')
    post = models.ForeignKey('Post', blank=False, on_delete=models.CASCADE, related_name='comments', verbose_name="пост")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', null=True, default=None)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="время изменения")

    def __str__(self):
        return f'Author: {self.author} \n Text: {self.text} \n Post: {self.post} \n Data: {self.time_update}'

    class Meta:
        ordering = ['-time_create']
