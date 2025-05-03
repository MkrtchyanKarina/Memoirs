menu = [
    {'title': "Главная страница", 'url_name': 'home_page'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить пост", 'url_name': 'add_post'},
    # {'title': "Ваши посты", 'url_name': 'my_posts'},
]


class DataMixin:
    paginate_by = 3  # постраничная навигация для всех классов представления, унаследованных от базового класса ListView
    title = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        if self.title:
            self.extra_context['title'] = self.title

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected


    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context.update(kwargs)

        return context
