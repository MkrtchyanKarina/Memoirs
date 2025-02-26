from django import template
import post.views as views

register = template.Library()


@register.simple_tag()
def get_categories():
    return views.categories_db


@register.inclusion_tag('post/list_categories.html')
def show_categories(cat_selected=0):
    categories = views.categories_db
    return {'categories': categories, 'cat_selected': cat_selected}
