import os
import prosto_sms
import stripe
from django.shortcuts import redirect
from config.settings import STRIPE_API_KEY
from users.models import User
import random

stripe.api_key = STRIPE_API_KEY

AMOUNT = 50

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
        success_url="https://example.com/success",
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


def send_token(phone, key):
    """Функция отправки СМС клиенту"""
    api = prosto_sms.API(
        email=os.getenv('EMAIL_SMS'),
        password=os.getenv('PASSWORD_SMS')
    )
    sender_name = os.getenv('SENDER_NAME_SMS')
    api.methods.push_message(text=f'Код для регистрации на сайте "Backers" {key}', phone=f'{phone}', sender_name=f'{sender_name}')

    return redirect('users:confirm_phone')


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