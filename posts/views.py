from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from posts.forms import PostForm
from posts.models import Post


class PostsListView(ListView):
    """Представление списка публикаций"""
    model = Post

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Post.objects.all()
        queryset = Post.objects.filter(is_active=True)
        return queryset


class PostsCreateView(LoginRequiredMixin, CreateView):
    """Представление создания публикации"""
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts:index')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PostsDetailView(DetailView):
    """Представление для просмотра одной публикации"""
    model = Post
    success_url = reverse_lazy('posts:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['posts'] = Post.objects.filter(id=self.kwargs.get('pk'))
        return context_data


class PostsUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для обновления одной публикации"""
    model = Post
    form_class = PostForm
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse('posts:view', args=[self.kwargs.get('pk')])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PostsDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для обновления одной публикации"""
    model = Post
    success_url = reverse_lazy('posts:index')
    login_url = reverse_lazy('users:login')


@login_required
def main_public(request):
    """Представление для отображения публикаций пользователя"""
    posts_list = Post.objects.filter(author_id=request.user.pk)
    posts_count_all = Post.objects.filter(author_id=request.user.pk).count()
    posts_count_active = Post.objects.filter(
        author_id=request.user.pk,
        is_active=True
    ).count()
    posts_count_pay = Post.objects.filter(
        author_id=request.user.pk,
        is_pay=True
    ).count()

    context_data = {
        'posts_count_all': posts_count_all,
        'posts_count_active': posts_count_active,
        'posts_count_pay': posts_count_pay,
        'posts_list': posts_list
    }

    return render(request, 'posts/user_posts.html', context_data)