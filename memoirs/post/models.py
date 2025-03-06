from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    """ Класс, описывающий структуру таблицы в БД. Экземпляр этого класса - конкретная запись в созданной таблице """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)  # blank=True - поле необязательно для заполнения
    time_create = models.DateTimeField(auto_now_add=True)  # auto_now_add=True - поле задается только
    # при создании записи и больше не изменяется
    time_update = models.DateTimeField(auto_now=True)  # auto_now=True - поле меняется при каждом изменении записи
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)  # default=True - по умолчанию статья опубликована

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})
