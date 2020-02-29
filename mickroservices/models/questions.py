from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class QuestionModel(models.Model):
    """docstring for QuestionModel"""

    ST_CONSIDERATION, ST_OK, ST_REJECTED = range(3)
    STATUS_CHOICE = (
        (ST_CONSIDERATION, "На рассмотрении"),
        (ST_OK, "Одобрено"),
        (ST_REJECTED, "Отклонено"),
    )

    name = models.CharField(max_length=255, blank=False, null=False,
                            verbose_name='Имя отправителя')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_faq', blank=True, null=True)
    phone_number = PhoneNumberField(null=True, blank=True,
                                    verbose_name='Номер телефона')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    theme = models.CharField(max_length=100, blank=False, null=False,
                             verbose_name='Тема')
    body = models.CharField(max_length=1000, blank=False, null=False,
                            verbose_name='Сообщение')
    status = models.IntegerField(choices=STATUS_CHOICE, default=ST_CONSIDERATION)
    answer = models.CharField(max_length=1000, blank=False, null=False,
                              verbose_name='Ответ')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    hide = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Вопрос от пользователя'
        verbose_name_plural = 'Вопросы от пользоватлей'
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.theme} от {self.name}'
