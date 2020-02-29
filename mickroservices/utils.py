from django.conf import settings
from django.core.mail import EmailMessage
# from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

import logging


def send_message(template, ctx, subject, to_email, request=None,
                 from_email=settings.DEFAULT_FROM_EMAIL):
    '''Отправка электронных писем'''
    if request:
        current_site = get_current_site(request)
        domain = current_site.domain
    else:
        domain = settings.DEFAULT_DOMAIN

    ctx.update({'protocol': settings.DEFAULT_PROTOCOL, 'domain': domain})
    message = render_to_string(template, ctx)
    if isinstance(to_email, str):
        to_email = [to_email]
    msg = EmailMessage(subject=subject, body=message,
                       to=to_email,
                       from_email=from_email)
    msg.content_subtype = 'html'
    try:
        msg.send()
    except Exception as e:
        print('There was an error sending an email: ', e)
        logging.error('Ошибка отправки письма . Причина: %s', str(e), exc_info=True)
        return e
