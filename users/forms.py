from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    class Meta:
        model = User
        fields = ('phone', 'avatar', 'city', 'first_name', 'last_name')

    def clean_phone(self):
        """Валидация номера телефона"""
        cleaned_data = self.cleaned_data['phone']

        if int(cleaned_data[0]) != 8:
            raise forms.ValidationError('Номер телефона должен начинаться с 8. ')
        elif not cleaned_data.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')
        elif len(cleaned_data) != 11:
            raise forms.ValidationError(f'Номер телефона должен состоять из 11 символов {len(cleaned_data)}')

        return cleaned_data


class UserForm(UserChangeForm):
    """Форма для пользователя"""

    class Meta:
        model = User
        fields = ['phone', 'password', 'avatar', 'city', 'first_name', 'last_name']

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