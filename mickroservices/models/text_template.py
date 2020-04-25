from django.urls import reverse
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel


class TextTemplate(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    class Meta:
        verbose_name = "Текстовый шаблон"

    def get_context(self, request, **kwargs):
        context = super(TextTemplate, self).get_context(request)
        context['breadcrumb'] = [
            {'title': self.title}
        ]
        return context


class Blog(Page):
    body = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Фоновая картинка'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        ImageChooserPanel('image'),
    ]

    class Meta:
        verbose_name = "Блог"

    def get_context(self, request, **kwargs):
        context = super(Blog, self).get_context(request)
        context['breadcrumb'] = [
            {'title': 'Блог',
             'url': reverse('mickroservices:blogs')},
            {'title': self.title}
        ]
        return context
