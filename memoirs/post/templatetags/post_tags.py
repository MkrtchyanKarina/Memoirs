from django import template
import post.views as views
from post.models import Category, TagPost
register = template.Library()


@register.inclusion_tag('post/list_categories.html')
def show_categories(cat_selected=0):
    categories = Category.objects.all()
    return {'categories': categories, 'cat_selected': cat_selected}


@register.inclusion_tag('post/list_tags.html')
def show_all_tags():
    tags = TagPost.objects.all()
    return {'tags': tags}
