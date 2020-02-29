from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class IdeaModel(models.Model):
    """docstring for IdeaModel"""

    ST_CONSIDERATION, ST_OK, ST_REJECTED = range(3)
    STATUS_CHOICE = (
        (ST_CONSIDERATION, "На рассмотрении"),
        (ST_OK, "Одобрено"),
        (ST_REJECTED, "Отклонено"),
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sender_idea', blank=True, null=True)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipient_idea', blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    phone_number = PhoneNumberField(null=True, blank=True,
                                    verbose_name='Номер телефона')    
    body = models.CharField(max_length=1000, blank=False, null=False,
                            verbose_name='Сообщение')
    status = models.IntegerField(choices=STATUS_CHOICE, default=ST_CONSIDERATION)
    answer = models.CharField(max_length=1000, blank=False, null=False,
                              verbose_name='Ответ')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_answer = models.DateTimeField(auto_now_add=True, verbose_name='Дата оповещения автора')
    file = models.FileField(upload_to='ideas', blank=True)

    class Meta:
        verbose_name = 'Идея от пользователя'
        verbose_name_plural = 'Идеи от пользоватлей'
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.body} от {self.email}'
