from django.db import models


class Post(models.Model):
    """ Класс, описывающий структуру таблицы в БД. Экземпляр этого класса - конкретная запись в созданной таблице """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)  # blank=True - поле необязательно для заполнения
    time_create = models.DateTimeField(auto_now_add=True)  # auto_now_add=True - поле задается только
    # при создании записи и больше не изменяется
    time_update = models.DateTimeField(auto_now=True)  # auto_now=True - поле меняется при каждом изменении записи
    is_published = models.BooleanField(default=True)  # default=True - по умолчанию статья опубликована

    def __str__(self):
        return self.title
