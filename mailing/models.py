from django.db import models

from config import settings


class Recipient(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец")
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

        # Права для менеджеров
        permissions = [
            ("can_view_all_recipients", "Может просматривать всех получателей"),
        ]

    def __str__(self):
        return self.full_name


class Message(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец")
    subject = models.CharField(max_length=255)
    body = models.TextField()

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

        # Права для менеджеров
        permissions = [
            ("can_view_all_messages", "Может просматривать все сообщения"),
        ]

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=[
            ("created", "Создана"),
            ("started", "Запущена"),
            ("completed", "Завершена"),
        ],
        default="created",
    )
    message = models.ForeignKey("Message", on_delete=models.CASCADE)
    recipients = models.ManyToManyField("Recipient")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

        # Права для менеджеров
        permissions = [
            ("can_view_all_mailings", "Может просматривать все рассылки"),
        ]

    def __str__(self):
        return f"{self.message.subject} - {self.status}"


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("failed", "Не успешно"),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField(blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mailing} - {self.status}"

