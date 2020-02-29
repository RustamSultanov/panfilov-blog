from django.db import models
from django.urls import reverse

from wagtail.admin.edit_handlers import FieldPanel

from mickroservices.models import TextTemplate


class MarketingMaterial(TextTemplate):
    (T_PROMOTIONS, T_BEFORE_OPENING, T_MENU,
     T_OTHER_LAYOUTS, T_VIDEOS, T_AUDIO_CLIPS) = range(6)

    TYPE_CHOICE = (
        (T_PROMOTIONS, 'Акции'),
        (T_BEFORE_OPENING, 'Перед открытием'),
        (T_MENU, 'Меню'),
        (T_OTHER_LAYOUTS, 'Другие макеты'),
        (T_VIDEOS, 'Видеоролики'),
        (T_AUDIO_CLIPS, 'Аудиоролики')
    )

    type = models.SmallIntegerField(
        choices=TYPE_CHOICE, default=T_PROMOTIONS, verbose_name='Тип')

    content_panels = [
        FieldPanel('type'),
    ] + TextTemplate.content_panels

    template = 'mickroservices/text_template.html'

    class Meta:
        verbose_name = "Маркетинговые материалы"

    @property
    def type_str(self):
        return self.TYPE_CHOICE[self.type][1]

    def get_context(self, request):
        context = super(MarketingMaterial, self).get_context(request)
        context['breadcrumb'] = [
            {'title': 'Маркетинговые материалы',
             'url': reverse('mickroservices:marketing')},
            {'title': self.title}
        ]
        return context
