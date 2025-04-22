from post.utils import menu


def get_posts_context(request):
    """ Контекстный процессор для отображения главного меню в базовом шаблоне
    request: данные о запросе
    return: возвращаем словарь с меню по ключу mainmenu
    """
    return {'mainmenu': menu}