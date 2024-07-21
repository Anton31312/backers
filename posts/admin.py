from django.contrib import admin
from .models import Post


@admin.register(Post)
class Publication(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_active', 'is_pay',)
    list_filter = ('author', 'is_active', 'is_pay',)