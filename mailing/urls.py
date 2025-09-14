from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    HomeView,
    MailingAttemptListView,
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingListView,
    MailingUpdateView,
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
    RecipientCreateView,
    RecipientDeleteView,
    RecipientDetailView,
    RecipientListView,
    RecipientUpdateView,
    UserStatsView,
    send_mailing,
    toggle_mailing_status,
)

app_name = "mailing"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path(
        "recipients/<int:pk>/",
        cache_page(60)(RecipientDetailView.as_view()),
        name="recipient_detail",
    ),
    path(
        "recipients/create/",
        RecipientCreateView.as_view(),
        name="recipient_create",
    ),
    path(
        "recipients/<int:pk>/update/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipients/<int:pk>/delete/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    # Сообщения
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/<int:pk>/", cache_page(60)(MessageDetailView.as_view()), name="message_detail"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "messages/<int:pk>/update/",
        MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "messages/<int:pk>/delete/",
        MessageDeleteView.as_view(),
        name="message_delete",
    ),
    # Рассылки
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/<int:pk>/", cache_page(60)(MailingDetailView.as_view()), name="mailing_detail"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailings/<int:pk>/update/",
        MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailings/<int:pk>/delete/",
        MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path("stats/", UserStatsView.as_view(), name="user_stats"),
    path(
        "mailing/toggle/<int:mailing_id>/",
        toggle_mailing_status,
        name="toggle_mailing_status",
    ),
    path(
        "mailing-attempts/",
        MailingAttemptListView.as_view(),
        name="mailing_attempt_list",
    ),
    path("mailings/<int:mailing_id>/send/", send_mailing, name="send_mailing"),

]
