from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Класс создания менеджера"""
    def handle(self, *args, **options):
        user = User.objects.create(
            phone='87776665544',
            first_name='Alex',
            last_name='Richards',
            is_staff=True,
            is_superuser=False,
            is_active=True
        )

        user.set_password('123qwe456rty')
        user.save()