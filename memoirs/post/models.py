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

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED)

    cat = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="posts")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        """  Возвращает строковое представление поста (его заголовок). """
        return self.title

    class Meta:
        verbose_name = "Все посты"
        verbose_name_plural = "Все посты"
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
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

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