from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

NULLABLE = {'blank': True, 'null': True}

class Post(models.Model):
    """Модель публикации"""
    title = models.CharField(max_length=250, verbose_name='заголовок')
    body = models.TextField(verbose_name='текст')
    photo = models.ImageField(upload_to='posts/', verbose_name='изображение', **NULLABLE)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    is_pay = models.BooleanField(default=False, verbose_name='платная публикация')
    is_active = models.BooleanField(default=True, verbose_name='скрыть/показывать')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="автор")

    def __str__(self):
        return

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'