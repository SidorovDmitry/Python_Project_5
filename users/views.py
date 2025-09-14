import secrets

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import CustomUserRegistrationForm, UserProfileForm

User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy("mailing:home")  # Перенаправление на главную страницу после успешной регистрации
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Пользователь неактивен до подтверждения почты
        user.save()
        self.send_verification_email(user)  # Отправка письма для подтверждения регистрации
        self.send_welcome_email(user.email)  # Отправка приветственного письма
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        """Отправка приветственного письма."""
        subject = "Добро пожаловать в наш сервис!"
        message = "Спасибо, что зарегистрировались в нашем сервисе рассылок!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)

    def send_verification_email(self, user):
        """Отправка письма с ссылкой для подтверждения почты."""
        token = secrets.token_hex(16)
        user.token = token  # Сохраняем токен в модели пользователя
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        subject = "Подтверждение регистрации"
        message = f"Для подтверждения регистрации перейдите по ссылке: {url}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)


def email_verification(request, token):
    """Подтверждение регистрации через токен."""
    user = get_object_or_404(User, token=token)
    user.is_active = True  # Активируем пользователя
    user.token = None  # Очищаем токен после подтверждения
    user.save()
    return redirect(reverse_lazy("users:login"))  # Перенаправляем на страницу входа


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.none()  # Обычные пользователи не видят список


def toggle_user_block(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет прав для выполнения этого действия.")

    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active  # Переключаем статус активности
    user.save()
    return redirect("user_list")


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        return self.request.user


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class CustomLoginView(LoginView):
    template_name = "users/login.html"  # Указываем путь к шаблону
    redirect_authenticated_user = True  # Если пользователь уже авторизован, перенаправляем на другую страницу
    success_url = reverse_lazy("mailing:home")  # Страница после успешного входа

    def get_success_url(self):
        return self.success_url  # Возвращаем URL для перенаправления после входа


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("mailing:home")