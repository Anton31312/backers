from celery import shared_task
from users.utils import change_is_pays, clean_tokens


@shared_task
def change_is_pays():
    change_is_pays()


@shared_task
def clean_tokens():
    clean_tokens()