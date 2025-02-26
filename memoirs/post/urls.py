from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='home_page'),
    path('about/', views.about, name="about"),
    # path('post/<int:post_id>/', views.show_post, name="post"),
    path('add-post/', views.add_post, name="add_post"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.login, name="login"),
    path('category/<int:cat_id>/', views.show_category, name="category")

]