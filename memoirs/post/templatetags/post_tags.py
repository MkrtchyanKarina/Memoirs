from django import template
import post.views as views
from django.db.models import Count, Q
from post.models import Category, TagPost
register = template.Library()



@register.inclusion_tag('post/list_categories.html')
def show_categories(cat_selected=0):
    categories = Category.objects.annotate(total=Count('posts', filter=Q(posts__is_published=1))).filter(total__gt=0)

    return {'categories': categories, 'cat_selected': cat_selected}


@register.inclusion_tag('post/list_tags.html')
def show_all_tags():
    tags = TagPost.objects.annotate(total=Count('tags', filter=Q(tags__is_published=1))).filter(total__gt=0)
    return {'tags': tags}
