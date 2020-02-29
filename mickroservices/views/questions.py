from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from mickroservices.models import QuestionModel
from mickroservices.forms import QuestionForm
from mickroservices.utils import send_message

from chat.models import Message as Chat_Message


class QuestionView(FormView):
    """ """    
    template_name = 'faq.html'
    success_url = reverse_lazy('faq')
    form_class = QuestionForm

    def get_context_data(self, **kwargs):
        ctx = super(QuestionView, self).get_context_data(**kwargs)
        questions_ok_list= QuestionModel.objects.filter(status=QuestionModel.ST_OK)
        ctx['breadcrumb'] = [{'title': 'FAQ'}]

        paginator = Paginator(questions_ok_list, 5)
        page = self.request.GET.get('page')
        try:
            ctx['questions_ok'] = paginator.page(page)
        except PageNotAnInteger:
            ctx['questions_ok'] = paginator.page(1)
        except EmptyPage:
            ctx['questions_ok'] = paginator.page(paginator.num_pages)
        ctx['is_paginated'] = paginator.num_pages > 1
        return ctx

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        ctx = self.get_context_data(**kwargs)
        if form.is_valid():
            self.form_valid(form)
            ctx.update(self.form_valid_send_message(
                       form,
                       'Обращение в техподдержку',
                       settings.DEFAULT_SUPORT_EMAIL,
                       self.get_context_data(**kwargs)))
            ctx['status'] = 'Ваш вопрос принят на рассмотрение!'
            ctx.pop('errors')
        else:
            ctx['errors'] = f'Ошибка заполнения полей: {form.errors}'

        return TemplateResponse(request, self.template_name, ctx)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.name = self.request.user.get_full_name()
        form.user = self.request.user
        form.save()
        Chat_Message.objects.create(
            sender=self.request.user,
            recipient=self.request.user.user_profile.manager.user,
            body="Был задан вопрос",
            question=form
        )

    def form_valid_send_message(self, form, subject, to_email, ctx):
        if form.is_valid():
            error = send_message(template='emails/email_question.html',
                                 subject=subject,
                                 ctx={},
                                 to_email=to_email,
                                 request=self.request)
            if not error:

                ctx['status'] = 'email_send'
            else:
                ctx['errors'] = 'Ошибка отправления письма'
        else:
            ctx['errors'] = 'Что-то пошло не так: одно из полей было заполнено некорректно. Повторите попытку отправки формы.'
        return ctx
