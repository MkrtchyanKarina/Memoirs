from django.urls import path
from . import views



urlpatterns = [
    path('', views.PostHome.as_view(), name='home_page'),
    path('about/', views.about, name="about"),
    path('post/<int:post_id>/', views.ShowPost.as_view(), name="post"),
    path('add-post/', views.AddPost.as_view(), name="add_post"),
    path('category/<slug:cat_slug>/', views.PostCategory.as_view(), name="category"),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name="tag"),
    path('edit-post/<int:pk>/', views.UpdatePost.as_view(), name="edit_post"),
    path('delete-post/<int:pk>/', views.DeletePost.as_view(), name="delete_post"),
    path('users-posts/<int:user_id>/', views.UsersPostsList.as_view(), name='users_posts'),

    path('add-comm/post/<int:post_id>/', views.AddComment.as_view(), name="add_comm"),

]