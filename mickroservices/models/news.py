from django.db import models
from django.urls import reverse
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class NewsPage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    preview = RichTextField(blank=True)
    body = RichTextField(blank=True)
    announcement = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        ImageChooserPanel('image'),
    ]

    class Meta:
        verbose_name = "Программы"

    def get_context(self, request, **kwargs):
        context = super(NewsPage, self).get_context(request)
        context['breadcrumb'] = [
            {'title': 'Программы',
             'url': reverse('mickroservices:news')},
            {'title': self.title}
        ]
        return context
