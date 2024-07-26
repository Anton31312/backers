from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    class Meta:
        model = User
        fields = ('phone', 'nickname', 'avatar', 'city', 'first_name', 'last_name', 'password1', 'password2')



class UserForm(UserChangeForm):
    """Форма для пользователя"""

    class Meta:
        model = User
        fields = ['phone', 'nickname', 'password', 'avatar', 'city', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
        for field_name, field in self.fields.items():
            if field_name not in ['avatar', 'is_active_mail']:
                field.widget.attrs['class'] = 'form-control'


class GetTokenForm(forms.Form):
    """Форма получения токена от пользователя"""
    phone = forms.CharField(widget=forms.TextInput())
    token = forms.CharField(widget=forms.TextInput())


class NewTokenForm(forms.Form):
    """Форма повторной отправки токена"""
    phone = forms.CharField(widget=forms.TextInput())