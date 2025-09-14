from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class StyleFormMixin:
    """Миксин для стилизации полей формы."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.EmailField):
                field.widget.attrs.update({"class": "form-control", "type": "email"})
            else:
                field.widget.attrs.update({"class": "form-control"})


class CustomUserRegistrationForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя."""

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )


class UserProfileForm(UserChangeForm):
    password = None  # Убираем поле пароля

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name")
