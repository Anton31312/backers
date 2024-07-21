from django import forms
from posts.models import Post


class PostForm(forms.ModelForm):
    """Форма публикации"""
    class Meta:
        model = Post
        fields = ['title', 'body', 'photo', 'is_active', 'is_pay', 'author',]

    def __init__(self, user, *args, **kwargs, ):
        self.user = user
        super(PostForm, self).__init__(*args, **kwargs)

        if not self.user.is_vip:
            del self.fields['is_pay']

        for field_name, field in self.fields.items():
            if field_name != 'is_pay' and field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'