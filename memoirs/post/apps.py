from django.apps import AppConfig


class PostConfig(AppConfig):
    verbose_name = "Посты"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post'
