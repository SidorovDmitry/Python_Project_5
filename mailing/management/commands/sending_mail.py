from django.core.management.base import BaseCommand

from mailing.models import Mailing
from mailing.services import perform_mailing


class SendingMail(BaseCommand):
    help = "Выполнение всех активных рассылок"

    def handle(self, *args, **kwargs):
        active_mailings = Mailing.objects.filter(status="created")
        for mailing in active_mailings:
            self.stdout.write(f"Начинаю рассылку {mailing.id}...")
            perform_mailing(mailing.id)
            self.stdout.write(f"Рассылка {mailing.id} завершена.")
