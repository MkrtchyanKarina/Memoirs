from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Post, Category



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """ Класс для настройки отображения статей в админ-панели """
    fields = ['title', 'content', 'author', 'cat', 'tags', 'is_published', 'images', 'post_images']
    # exclude = ['tags']
    readonly_fields = ['is_published', 'post_images']
    filter_horizontal = ('tags', )


    list_display = ('title', 'time_create', 'is_published', 'cat', 'post_images')  # поля, которые отображаются в списке статей
    list_display_links = ('title', )  # сделаем оба поля id и title кликабельными

    ordering = ['-time_create', 'title']  # сортировка статей по дате и времени добавления (в обратном порядке), а также по названию
    list_editable = ('is_published', )  # кликабельное поле не может быть редактируемым
    list_per_page = 5

    actions = ['set_published', 'set_draft']  # добавим новый метод изменения записей в поле actions

    search_fields = ['title__startswith', 'cat__name']  # добавим поля для поиска

    list_filter = ['cat__name', 'is_published', 'tags__tag']  # добавим боковую панель фильтров

    save_on_top = True  # отобразим панель с кнопками сохранения и удаления сверху статьи


    @admin.display(description="Фото")
    def post_images(self, post: Post):
        """
        Функция для отображения фотографии, связанной с данным постом
        """
        if post.images:
            return mark_safe(f"<img src='{post.images.url}', width=50>")
        else:
            return "Фото отсутствует"


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
    prepopulated_fields = {'slug': ('name', )}  # автоматическое заполнение поля slug на основе названия категории - name
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')


