from django.contrib import admin, messages
from .models import Post, Category



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """ Класс для настройки отображения статей в админ-панели """
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')  # поля, которые отображаются в списке статей
    list_display_links = ('title', )  # сделаем оба поля id и title кликабельными

    ordering = ['-time_create', 'title']  # сортировка статей по дате и времени добавления (в обратном порядке), а также по названию
    list_editable = ('is_published', )  # кликабельное поле не может быть редактируемым
    list_per_page = 5

    actions = ['set_published', 'set_draft']  # добавим новый метод изменения записей в поле actions

    search_fields = ['title__startswith', 'cat__name']  # добавим поля для поиска

    list_filter = ['cat__name', 'is_published', 'tags__tag']  # добавим боковую панель фильтров


    @admin.display(description="краткое описание", ordering='content')
    def brief_info(self, post: Post):
        """
        Функция для отображения дополнительного столбца с количеством символов записи
        :param post: экземпляр класса Post, т.е. определенная запись из таблицы Постов
        """
        return f"Описание: {len(post.content)} символов"


    @admin.display(description="Опубликовать выбранные Посты")
    def set_published(self, request, queryset):
        """
        Метод для изменения статуса на "Опубликовано" для выбранных статей
        :param request: объект запроса (информация о текущем http-запросе)
        :param queryset: набор выбранных записей
        """
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.", messages.INFO)


    @admin.display(description="Снять с публикации")
    def set_draft(self, request, queryset):
        """
        Метод для изменения статуса на "Черновик" для выбранных статей
        :param request: объект запроса (информация о текущем http-запросе)
        :param queryset: набор выбранных записей
        """
        count = queryset.update(is_published=Post.Status.DRAFT)
        self.message_user(request, f"{count} записей снято с публикации!", messages.WARNING)






@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')


