from django import template
import post.views as views
from post.models import Category
register = template.Library()


@register.inclusion_tag('post/list_categories.html')
def show_categories(cat_selected=0):
    categories = Category.objects.all()
    return {'categories': categories, 'cat_selected': cat_selected}
