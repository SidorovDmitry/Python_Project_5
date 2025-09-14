from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from mailing.models import Mailing, Message, Recipient


class Command(BaseCommand):
    help = 'Создает группу "Менеджеры" с необходимыми правами'

    def handle(self, *args, **kwargs):
        # Создание группы
        group, created = Group.objects.get_or_create(name="Менеджеры")

        # Назначение прав для модели Mailing
        mailing_content_type = ContentType.objects.get_for_model(Mailing)
        mailing_permissions = Permission.objects.filter(
            content_type=mailing_content_type, codename__in=["can_view_all_mailings"]
        )
        group.permissions.add(*mailing_permissions)

        # Назначение прав для модели Message
        message_content_type = ContentType.objects.get_for_model(Message)
        message_permissions = Permission.objects.filter(
            content_type=message_content_type, codename__in=["can_view_all_messages"]
        )
        group.permissions.add(*message_permissions)

        # Назначение прав для модели Recipient
        recipient_content_type = ContentType.objects.get_for_model(Recipient)
        recipient_permissions = Permission.objects.filter(
            content_type=recipient_content_type,
            codename__in=["can_view_all_recipients"],
        )
        group.permissions.add(*recipient_permissions)

        self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" успешно создана!'))
