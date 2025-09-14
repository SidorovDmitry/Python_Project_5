from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

# Правильный импорт настроек
from django.conf import settings

from .models import Mailing, MailingAttempt, Message, Recipient


def send_email(recipient_email, subject, body):
    """
    Отправляет email-сообщение получателю.

    :param recipient_email: Email адрес получателя
    :param subject: Тема письма
    :param body: Тело письма
    :return: Кортеж (успешно: bool, ответ сервера: str)
    """
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return True, None
    except Exception as e:
        return False, str(e)


def perform_mailing(mailing_id):
    """
    Выполняет рассылку по указанному ID.

    :param mailing_id: ID рассылки
    """
    try:
        mailing = Mailing.objects.get(id=mailing_id)
        if mailing.status == "completed":
            return  # Если рассылка уже завершена, ничего не делаем

        mailing.status = "started"
        mailing.save()

        for recipient in mailing.recipients.all():
            success, response = send_email(
                recipient.email,
                mailing.message.subject,
                mailing.message.body
            )
            MailingAttempt.objects.create(
                status="success" if success else "failed",
                server_response=response if not success else None,
                mailing=mailing,
            )

        mailing.status = "completed"
        mailing.save()

    except Mailing.DoesNotExist:
        print(f"Рассылка с ID {mailing_id} не найдена")
    except Exception as e:
        print(f"Error during mailing: {e}")


def get_recipients_from_cache(user=None):
    """
    Получает получателей из кэша или базы данных.

    :param user: Пользователь для фильтрации (опционально)
    :return: QuerySet получателей
    """
    # Получаем настройку кэша из settings
    cache_enabled = getattr(settings, 'CACHE_ENABLED', False)

    if not cache_enabled:
        if user and not user.is_staff:
            return Recipient.objects.filter(owner=user)
        return Recipient.objects.all()

    # Формируем ключ кэша в зависимости от пользователя
    if user and not user.is_staff:
        key = f"recipient_list_user_{user.id}"
        queryset = Recipient.objects.filter(owner=user)
    else:
        key = "recipient_list_all"
        queryset = Recipient.objects.all()

    recipients = cache.get(key)
    if recipients is not None:
        return recipients

    recipients = list(queryset)
    cache.set(key, recipients, 300)  # Кэшируем на 5 минут
    return recipients


def get_messages_from_cache(user=None):
    """
    Получает сообщения из кэша или базы данных.

    :param user: Пользователь для фильтрации (опционально)
    :return: QuerySet сообщений
    """
    # Получаем настройку кэша из settings
    cache_enabled = getattr(settings, 'CACHE_ENABLED', False)

    if not cache_enabled:
        if user and not user.is_staff:
            return Message.objects.filter(owner=user)
        return Message.objects.all()

    # Формируем ключ кэша в зависимости от пользователя
    if user and not user.is_staff:
        key = f"message_list_user_{user.id}"
        queryset = Message.objects.filter(owner=user)
    else:
        key = "message_list_all"
        queryset = Message.objects.all()

    messages = cache.get(key)
    if messages is not None:
        return messages

    messages = list(queryset)
    cache.set(key, messages, 300)  # Кэшируем на 5 минут
    return messages