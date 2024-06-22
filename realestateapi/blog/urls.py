from django.urls import path

from .views import create_post, get_post, update_post,create_tag

urlpatterns = [
    path('posts/<int:pk>/update', update_post, name='posts-update'),
    path('posts/<int:pk>', get_post, name='posts-get'),
    path('posts/', create_post, name='posts-create'),
    path('tag/', create_tag, name='posts-create'),
]
