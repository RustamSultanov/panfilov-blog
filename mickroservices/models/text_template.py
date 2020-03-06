from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


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

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    class Meta:
        verbose_name = "Блог"

    def get_context(self, request, **kwargs):
        context = super(Blog, self).get_context(request)
        context['breadcrumb'] = [
            {'title': self.title}
        ]
        return context
