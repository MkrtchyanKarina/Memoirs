from django.urls import path
from . import views



urlpatterns = [
    path('', views.PostHome.as_view(), name='home_page'),
    path('about/', views.about, name="about"),
    path('post/<int:post_id>/', views.ShowPost.as_view(), name="post"),
    path('add-post/', views.AddPost.as_view(), name="add_post"),  # передаем не ссылку на класс, а вызываем его метод as_view
    path('contact/', views.contact, name="contact"),
    path('login/', views.login, name="login"),
    path('category/<slug:cat_slug>/', views.PostCategory.as_view(), name="category"),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name="tag"),

]