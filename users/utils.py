import string
import stripe
import random

from smsaero import SmsAero
from django.conf import settings




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
    stripe_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "rub",
                    "unit_amount": settings.PRODUCT_PRICE * 100,
                    "product_data": {
                        "name": "VIP подписка",
                    },
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url='http://127.0.0.1:8000/users/payment_success',
        cancel_url='http://127.0.0.1:8000/users/payment_cancel'
    )
    return stripe_session.get('id'), stripe_session.get('url')


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
    key = ''.join(random.choice(string.digits) for i in range(6))
    return key

