from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Класс создания админа"""
    def handle(self, *args, **options):
        user = User.objects.create(
            phone='89992223311',
            nickname='MainAdmin',
            first_name='Admin',
            last_name='Admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('123qwe456rty')
        user.save()