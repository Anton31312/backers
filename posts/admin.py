from django.contrib import admin
from posts.models import Post


@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_active', 'is_pay',)
    list_filter = ('author', 'is_active', 'is_pay',)