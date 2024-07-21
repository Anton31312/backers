from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from posts.models import Post
from users.models import User


class PostViewTest(TestCase):
    """Тест публикаций """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(phone='89992223311', password='qwe12#QQM', is_active=True)
        self.client.force_login(self.user)

    def test_get_post(self):
        """Тест создания публикации """
        response = self.client.get(reverse('posts:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')
        data = {
            'title': 'Test Post',
            'body': 'This is a test Post.',
        }
        response = self.client.post(reverse('posts:create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(Post.objects.all().filter(author_id=self.user).first().title, 'Test Post')

    def test_list(self):
        """Тест списка публикации """
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 0)

    def test_update(self):
        """Тест обновления публикации """
        self.post_update = Post.objects.all().filter(author_id=self.user).first()
        response = self.client.get(reverse_lazy('posts:update', kwargs={'pk': self.post_update.id}))
        self.assertEqual(response.status_code, 200)
        data = {'title': 'Updated test Post',
                'body': 'Updated test content'}
        response = self.client.post(reverse('posts:update', kwargs={'pk': self.post_update.id}), data=data)
        self.post_update.refresh_from_db()
        self.assertEqual(self.post_update.title, 'Updated test Post')
        self.assertEqual(self.post_update.body, 'Updated test content')

    def test_delete(self):
        """Тест удаления публикации """
        self.post_delete = Post.objects.all().filter(author_id=self.user).first()
        response = self.client.delete(reverse_lazy('posts:delete', args=[self.post_delete.id]))
        self.assertEqual(response.status_code, 204)
        
        self.assertEqual(Post.objects.count(), 0)