from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
    """Модель класса User"""

    username = None
    phone = PhoneNumberField(region='RU', verbose_name='номер телефона', unique=True)
    nickname = models.CharField(max_length=200, verbose_name='псевдоним', unique=True)
    avatar = models.ImageField(upload_to='unique', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=30, verbose_name='город', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активация пользователя')
    is_vip = models.BooleanField(default=False, verbose_name='VIP-клиент')
    token = models.CharField(max_length=100, verbose_name='токен', **NULLABLE)
    payment_session_id = models.CharField(max_length=300, verbose_name='ID сессии оплаты', **NULLABLE)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.nickname}'

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"