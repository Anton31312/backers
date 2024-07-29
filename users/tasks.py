from celery import shared_task

from users.models import User
from users.utils import retrieve_a_session


@shared_task
def change_is_pays():
    """Функция смены статуса пользователя на VIP"""
    users_unpaid = User.objects.filter(
        payment_session_id__isnull=False,
        is_vip=False
    )

    for user in users_unpaid:
        if retrieve_a_session(user.payment_session_id) == "paid":
            user.is_vip = True
            user.payment_session_id = None
            user.save()


@shared_task
def clean_tokens():
    """Функция очистки токенов"""
    User.objects.filter(token__isnull=False).update(token=None)