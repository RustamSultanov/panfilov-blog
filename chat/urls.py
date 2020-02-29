from django.urls import path
 

from .models import Message
from . import views

urlpatterns = [
    path(
        'close_message_chat/', views.close_message, name='close_message'),
]