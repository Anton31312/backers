from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Класс создания обычного пользователя"""
    def handle(self, *args, **options):
        user = User.objects.create(
            phone='86661112233',
            first_name='Petr',
            last_name='Petrov',
            is_staff=False,
            is_superuser=False,
            is_active=True
        )

        user.set_password('123qwe456rty')
        user.save()