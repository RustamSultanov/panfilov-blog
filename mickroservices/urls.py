from django.contrib.auth.decorators import login_required
from django.urls import path

from mickroservices import views

app_name = 'mickroservices'

urlpatterns = [
    path('faq/',
         login_required(views.QuestionView.as_view()),
         name='faq'),

    path('ideas/',
         login_required(views.IdeaView.as_view()),
         name='idea'),

    path('lessons/',
         login_required(views.CoursesView.as_view()),
         name='lessons'),
    path('lesson/<int:pk>',
         login_required(views.CourseView.as_view()),
         name='lesson'),

    path('news/',
         views.NewsView.as_view(),
         name='news'),
    path('news/new/',
         login_required(views.NewsCreateView.as_view()),
         name='news_new'),
    path('news/edit/<int:pk>',
         login_required(views.NewsEditView.as_view()),
         name='news_edit'),

    path('marketing/',
         login_required(views.MarketingView.as_view()),
         name='marketing'),

    path('schedule/<int:pk>',
         login_required(views.ScheduleView.as_view()),
         name='schedule_view'),
    path('schedule/new/',
         login_required(views.ScheduleCreateView.as_view()),
         name='schedule_new'),
    path('schedule/',
         login_required(views.ScheduleListView.as_view()),
         name='schedule'),
    path('tech_cards/',
         login_required(views.TechCardsListView.as_view()),
         name='tech_cards'),
    path('regulations/',
         login_required(views.RegulationsListView.as_view()),
         name='regulations'),    
]
