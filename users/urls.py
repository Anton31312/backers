from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.views import *

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm_phone/', get_token, name='confirm_phone'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('delete_user_danger', delete_user_danger, name='delete_user_danger'),
    path('payment_vip/', payment_vip, name='payment_vip'),
    path('user_list/', get_all_users, name='user_list'),
    path('activity/<int:pk>', toggle_activity_user, name='toggle_activity_user'),
    path('resending_token/', resending_token, name='resending_token'),
]