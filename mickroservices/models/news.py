from calendar import Calendar
from datetime import date, timedelta, datetime

from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from ls.joyous.models import getAllEventsByDay, RecurringEventPage
from psycopg2._range import DateTimeTZRange
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel




class NewsPage(Page):
    CL_ONE, CL_ONE_AND_ONE = range(2)
    CLASSES_CHOICE = (
        (CL_ONE, "Индивидуальная тренировка"),
        (CL_ONE_AND_ONE, "Индивидуальная тренировка 1+1"),
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Фоновая картинка'
    )
    subscription = models.BooleanField(default=False, verbose_name='Абонимент')
    places_limited = models.BooleanField(default=False, verbose_name='Ограничено мест')
    preview = RichTextField(blank=True, verbose_name='Превью для карточки')
    body = RichTextField(blank=True, verbose_name='Основная информация о программе')
    announcement = models.TextField(blank=True)
    cost = models.IntegerField(blank=True, verbose_name='Стоимость')
    type_classes = models.SmallIntegerField(choices=CLASSES_CHOICE, default=CL_ONE, verbose_name='Тип занятия')

    content_panels = Page.content_panels + [
        FieldPanel('preview', classname="full"),
        FieldPanel('cost'),
        FieldPanel('subscription'),
        FieldPanel('places_limited'),
        FieldPanel('body', classname="full"),
        ImageChooserPanel('image'),
    ]

    class Meta:
        verbose_name = "Программы"

    def get_context(self, request, **kwargs):
        context = super(NewsPage, self).get_context(request)
        today = timezone.localdate()
        c = Calendar()
        dates = list(c.itermonthdays3(today.year, today.month))
        date_select = date(today.year, today.month, today.day)
        ev = getAllEventsByDay(request, date_select, date_select)
        from sushi_app.forms import EventForm
        form = EventForm(request.POST or None, lst_events=ev[0].days_events)
        if form.is_valid():
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse_lazy("login"))
            rev = RecurringEventPage.objects.get(id=int(form.data['events']))
            dt = datetime.strptime(form.data['date'], "%d.%m.%Y")
            from sushi_app.models import Classes
            cl_ev = Classes(type_classes=self.type_classes,user=request.user, is_busy=True, duration=DateTimeTZRange(
                lower=dt + timedelta(minutes=rev.time_from.minute, hours=rev.time_from.hour - 3),
                upper=dt + timedelta(minutes=rev.time_to.minute, hours=rev.time_to.hour - 3)), recurrences_event=rev)
            cl_ev.save()
            return HttpResponseRedirect(reverse_lazy("ya_kassa"))
        context['calendar'] = [dates[i:i + 7] for i in range(0, len(dates), 7)]
        context['today'] = today
        context['form'] = form
        context['breadcrumb'] = [
            {'title': 'Программы',
             'url': reverse('mickroservices:news')},
            {'title': self.title}
        ]
        return context
