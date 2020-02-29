from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from mickroservices.models import IdeaModel
from mickroservices.forms import IdeaForm
from mickroservices.utils import send_message
from chat.models import Message as Chat_Message


class IdeaView(FormView):
    """ """
    template_name = 'idea.html'
    success_url = reverse_lazy('idea')
    form_class = IdeaForm

    def get_context_data(self, **kwargs):
        ctx = super(IdeaView, self).get_context_data(**kwargs)
        # ctx['ideas_ok'] = IdeaModel.objects.filter(status=IdeaModel.ST_OK)[:5]
        ctx['breadcrumb'] = [{'title': 'Идеи'}]
        return ctx

    def post(self, request, *args, **kwargs):
        form = IdeaForm(request.POST or None, request.FILES or None)
        ctx = self.get_context_data(**kwargs)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.sender = self.request.user
            idea.recipient = self.request.user.user_profile.manager.user
            idea.save()
            Chat_Message.objects.create(
                sender=self.request.user,
                recipient=self.request.user.user_profile.manager.user,
                body="Была предложена идея",
                idea=idea
            )
            ctx.update(self.form_valid_send_message(
                form,
                'Ваша идея принята на рассмотрение!',
                settings.DEFAULT_SUPORT_EMAIL,
                self.get_context_data(**kwargs)))
            ctx['status'] = 'Ваша идея принята на рассмотрение!'
            ctx.pop('errors')
        else:
            ctx['errors'] = f'Ошибка заполнения полей: {form.errors}'

        return TemplateResponse(request, self.template_name, ctx)

    def form_valid_send_message(self, form, subject, to_email, ctx):
        if form.is_valid():
            error = send_message(template='emails/email_idea.html',
                                 subject=subject,
                                 ctx={},
                                 to_email=to_email,
                                 request=self.request)
            if not error:

                ctx['status'] = 'email_send'
            else:
                ctx['errors'] = 'Ошибка отправления письма'
        else:
            ctx[
                'errors'] = 'Что-то пошло не так: одно из полей было заполнено некорректно. Повторите попытку отправки формы.'
        return ctx
