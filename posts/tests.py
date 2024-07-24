from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post
from users.models import User


class PostViewTest(TestCase):
    """
    Тестирование работы с публикациями
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(phone='88888888888', password='123456', is_active=True)
        self.post = Post.objects.create(title='Тест1', body='Описание теста1',
                                              author=self.user, is_pay=True)
        self.client.force_login(user=self.user)

    def test_create_posts(self):
        """
        Тестирование создания публикации
        """

        url = reverse('posts:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')
        data = {
            'title': 'Тест2',
            'body': 'Описание теста2',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(Post.objects.all().filter(author_id=self.user).first().body,
                         'Описание теста1')
        self.assertEqual(Post.objects.all().filter(author_id=self.user).count(), 2)

    def test_posts_list(self):
        """
        Тестирование списка публикаций
        """

        url = reverse('posts:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)

    def test_update_posts(self):
        """
        Тестирование обновления публикации
        """

        url = reverse('posts:update', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {
            'title': 'Тест1',
            'body': 'Новое описание теста',
        }
        response = self.client.post(url, data)
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.body, 'Новое описание теста')

    def test_delete_posts(self):
        """
        Тестирование удаления публикации
        """

        url = reverse('posts:delete', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.delete(url)
        self.assertEqual(Post.objects.count(), 0)

    def test_user_posts_list(self):
        """s
        Тестирование страницы публикаций для чтения
        """

        url = reverse('posts:user_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)