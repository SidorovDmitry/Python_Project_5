from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    ProfileEditView,
    ProfileView,
    RegisterView,
    UserListView,
    email_verification,
    toggle_user_block,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # Регистрация
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),  # Вход
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),  # Выход
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),  # Подтверждение почты
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",  # Шаблон письма
            success_url="/users/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url="/users/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/block/<int:user_id>/", toggle_user_block, name="toggle_user_block"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile_edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("logout-confirm/", CustomLogoutView.as_view(), name="logout_confirm"),
    path("login/", CustomLoginView.as_view(), name="login"),
]
