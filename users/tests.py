from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from users.models import User


class UserTest(TestCase):
    """Тест регистрации пользователя"""
    def setUp(self):
        pass
        self.client = Client()
        self.valid_data = {
            'phone': '89311111111',
            'avatar': 'avatar.jpg',
            'city': 'New York',
            'is_active': True,
            'is_vip': False,
            'token': '1111',
            'payment_session_id': 'session123',
            'password1': 'strong_password',
            'password2': 'strong_password',
        }

    def test_register(self):
        """Тест регистрации пользователя"""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_form.html')
        self.client.post(reverse('users:register'), data=self.valid_data)
        self.assertEqual(User.objects.count(), 0)

        """Тест обновления пользователя """
        self.user = User.objects.get(phone='89311111111')
        self.user.is_active = True
        self.user.save()
        self.client.force_login(user=self.user)
        self.client.is_active = True
        self.user_update = User.objects.all().filter(id=self.user.pk).first()
        response = self.client.get(reverse_lazy('users:profile'))
        self.assertEqual(response.status_code, 200)

        """Тест удаления пользователя """
        self.user = User.objects.get(phone='89311111111')
        self.user.is_active = True
        self.user.save()
        self.client.force_login(user=self.user)
        self.client.is_active = True
        self.user_delete = User.objects.all().filter(id=self.user.pk).first()
        response = self.client.get(reverse_lazy('users:delete_user', kwargs={'user_id': self.user_delete.id}))
        self.assertEqual(response.status_code, 302)
        self.client.delete(reverse_lazy('users:delete_user', kwargs={'user_id': self.user_delete.id}))
        self.assertEqual(User.objects.count(), 0)