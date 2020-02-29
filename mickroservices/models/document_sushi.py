from django.db import models
from wagtail.search import index
from wagtail.documents.models import Document

class Subjects(models.Model):
    (T_TEH_CARD, T_REGULATIONS, T_PROMOTIONS, T_BEFORE_OPEN,
     T_MENU, T_OTHER_MAKET, T_VIDEO, T_AUDIO,
     T_PERSONAL, T_PERSONAL_INVOICES, T_TRAINING)  = range(11)
    STATUS_CHOICE = (
        (T_TEH_CARD, "Техкарты"),
        (T_REGULATIONS, "Регламенты"),
        (T_PROMOTIONS, "Акции"),
        (T_BEFORE_OPEN, "Перед открытием"),
        (T_MENU, "Меню"),
        (T_OTHER_MAKET, "Другие макеты"),
        (T_VIDEO, "Видеоролики"),
        (T_AUDIO, "Аудиоролики"),
        (T_PERSONAL, "Личные документы"),
        (T_PERSONAL_INVOICES, "Личные счета"),
        (T_TRAINING, "Обучение"),
    )

    name = models.CharField(max_length=255, blank=False, null=False,
                            verbose_name='Наименование')
    type = models.SmallIntegerField(choices=STATUS_CHOICE, default=T_TEH_CARD)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тематика(папка)'
        verbose_name_plural = 'Тематики(папки)'


class DocumentSushi(Document):
    (T_TEH_CARD, T_REGULATIONS, T_PROMOTIONS, T_BEFORE_OPEN,
     T_MENU, T_OTHER_MAKET, T_VIDEO, T_AUDIO,
     T_PERSONAL, T_PERSONAL_INVOICES, T_TRAINING)  = range(11)
    STATUS_CHOICE = (
        (T_TEH_CARD, "Техкарты"),
        (T_REGULATIONS, "Регламенты"),
        (T_PROMOTIONS, "Акции"),
        (T_BEFORE_OPEN, "Перед открытием"),
        (T_MENU, "Меню"),
        (T_OTHER_MAKET, "Другие макеты"),
        (T_VIDEO, "Видеоролики"),
        (T_AUDIO, "Аудиоролики"),
        (T_PERSONAL, "Личные документы"),
        (T_PERSONAL_INVOICES, "Личные счета"),
        (T_TRAINING, "Обучение"),
    )

    doc_type = models.IntegerField(choices=STATUS_CHOICE, default=T_TEH_CARD)
    sub_type =  models.ForeignKey(Subjects, verbose_name='тематика',
                                  on_delete=models.CASCADE,
                                  related_name='documents',
                                  null=True,
                                  blank=True)

    search_fields = Document.search_fields +[
        index.SearchField('doc_type'),
        index.FilterField('doc_type'),
        index.FilterField('sub_type_id')
    ]


