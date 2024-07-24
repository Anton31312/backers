import stripe
import random

from smsaero import SmsAero
from django.conf import settings

from users.models import User


stripe.api_key = settings.STRIPE_API_KEY

AMOUNT = 50

def send_sms(phone: int, message: str):
    """Формирование отправки SMS-сообщения"""

    email = settings.SMSAERO_EMAIL
    if isinstance(email, tuple):
        email = email[0]
    key = settings.SMSAERO_API_KEY
    api = SmsAero(email, key)
    return api.send_sms(phone, message)


def create_sessions():
    """Функия создания сессии для оплаты с помощью сервиса Stripe"""
    # Сумма платежа
    amount = AMOUNT

    # Создание продукта
    product = stripe.Product.create(name='Платная подписка')

    # Создание цены
    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount,
        product=f'{product.id}',
    )

    # Создание сессии
    sessions = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/users/payment_success",
        cancel_url='http://127.0.0.1:8000/users/payment_cancel',
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return sessions


def retrieve_a_session(session_id):
    """Функция проверки статуса оплаты сессии Stripe"""

    sessions = stripe.checkout.Session.retrieve(
        f"{session_id}",
    )

    payment_status = sessions['payment_status']
    print('sessions=', sessions)
    return payment_status


def token_generate():
    """Функция генерации одноразового ключа"""
    key = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    return key


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


def clean_tokens():
    """Функция очистки токенов"""
    users_with_token = User.objects.filter(
        token__isnull=False,
    )

    for user in users_with_token:
        user.token = None
        user.save()