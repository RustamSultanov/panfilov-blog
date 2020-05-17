from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.utils.translation import ugettext_lazy
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.blocks import RawHTMLBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from django.db import models
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmetadata.models import MetadataMixin
from django.conf import settings


class MetadataPageMixin(MetadataMixin, models.Model):
    search_image = models.ForeignKey(
        get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    keywords = ArrayField(
        models.CharField(max_length=100, blank=True), null=True, blank=True)
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('show_in_menus'),
            FieldPanel('search_description'),
            FieldPanel('keywords'),
            ImageChooserPanel('search_image'),
        ], ugettext_lazy('Common page configuration')),
    ]
    _metadata = {
        "published_time": "published_time",
        "modified_time": "latest_revision_created_at",
        "expiration_time": "expire_at",
    }

    class Meta:
        abstract = True

    @property
    def published_time(self):
        return self.go_live_at or self.first_published_at

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return self.search_description

    def get_meta_keywords(self):
        return self.keywords or list()

    def get_meta_url(self):
        return self.build_absolute_uri(self.url)

    def get_meta_image(self):
        if self.search_image is not None:
            return self.build_absolute_uri(
                self.search_image.get_rendition(getattr(settings, "META_SEARCH_IMAGE_RENDITION", "fill-800x450")).url
            )
        return super(MetadataPageMixin, self).get_meta_image()

    def get_author(self):
        author = super(MetadataPageMixin, self).get_author()
        if hasattr(self, "owner") and isinstance(self.owner, get_user_model()):
            author.get_full_name = self.owner.get_full_name
        return author


class TextTemplate(MetadataPageMixin, Page):
    body = RichTextField(blank=True)
    extra_body = StreamField([
        ('table', RawHTMLBlock()),
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        StreamFieldPanel('extra_body'),
    ]

    class Meta:
        verbose_name = "Текстовый шаблон"

    def get_context(self, request, **kwargs):
        context = super(TextTemplate, self).get_context(request)
        context['breadcrumb'] = [
            {'title': self.title}
        ]
        return context


class Blog(MetadataPageMixin, Page):
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
