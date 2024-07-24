import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from smsaero import SmsAeroException

from users.forms import *
from users.utils import *


class RegisterView(CreateView):
    """Представление регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy('users:confirm_phone')

    def form_valid(self, form):
        self.object = form.save()
        phone = int(self.object.phone)
        token = ''.join(random.choice(string.digits) for i in range(6))
        self.object.token = token
        self.object.save()
        try:
            send_sms(phone=phone, message=f'Код подтверждения {token}')
            print('Сообщение отправлено')
        except SmsAeroException as e:
            print(f"An error occurred: {e}")
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Представление изменения данных пользователя"""
    model = UserRegisterForm,
    success_url = reverse_lazy('posts:index')
    form_class = UserRegisterForm

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def delete_user_danger(request):
    """Представление предупреждения удаления пользователя"""
    return render(request, 'users/user_delete.html')


@login_required
def delete_user(request, user_id):
    """Представление удаления пользователя"""
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect(reverse('posts:index'))


@login_required
def payment_vip(request):
    """Представление платежа"""
    user = request.user
    payment_session_id = create_sessions()["id"]
    user.payment_session_id = payment_session_id
    user.save()
    link = create_sessions()["url"]
    context_data = {'link': link}
    return render(request, 'users/payment_vip.html', context_data)

@login_required
def payment_success(request):
    """Отображение страницы при успешной оплате"""

    user = request.user
    user.is_vip = True
    user.save()

    return render(request, 'users/payment_success.html')


@login_required
def payment_cancel(request):
    """Отображение страницы при отмены оплаты"""
    return render(request, 'users/payment_cancel.html')

def get_all_users(request):
    """Функция получения пользователей"""
    users = User.objects.filter(
        is_staff=False,
        is_superuser=False,
    )
    return render(request, 'users/users_list.html', {'users': users})


def toggle_activity_user(request, pk):
    """Функция активации/деактивации пользователя"""
    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active:
        user_item.is_active = False
    else:
        user_item.is_active = True
    user_item.save()

    return redirect(reverse('users:user_list'))


def get_token(request):
    """Функция получения и проверки токена от клиента"""
    if request.method == 'POST':
        entered_token = request.POST.get('token', '')
        phone = request.POST.get('phone', '')
        user = get_object_or_404(User, phone=phone)
        if str(user.token) == str(entered_token):
            user.is_active = True
            user.save()
            return redirect('users:profile')
        else:
            return HttpResponse("Код подтверждения неверный. Попробуйте еще раз.")
    return render(request, 'users/confirm_phone.html')


def resending_token(request):
    """Повторной отправки токена клиенту"""
    if request.method == "POST":
        form = NewTokenForm(request.POST)
        if form.is_valid():
            phone = form.data["phone"]
            user = User.objects.get(phone=phone)
            token = token_generate()
            user.token = token
            user.save()
            send_sms(phone, token)

            return redirect(reverse('users:confirm_phone'))

    return render(request, 'users/confirm_phone.html', {'form': NewTokenForm})