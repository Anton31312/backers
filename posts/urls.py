from django.urls import path
from posts.apps import PostsConfig
from posts.views import *

app_name = PostsConfig.name

urlpatterns = [
    path('', PostsListView.as_view(), name='index'),
    path('create/', PostsCreateView.as_view(), name='create'),
    path('view/<int:pk>/', PostsDetailView.as_view(), name='view'),
    path('update/<int:pk>/', PostsUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PostsDeleteView.as_view(), name='delete'),
    path('user_posts/', main_public, name='user_posts'),
]