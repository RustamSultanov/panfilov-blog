from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy, include
from django_registration.backends.activation.views import RegistrationView

from . import views
from .forms import LoginForm, RegistrationCustomForm
from .views import YaKassaNotify

urlpatterns = [
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/reset/<uidb64>/<token>/',
         auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path(
        '', views.base, name='base'),
    path(
        'accounts/login/',
        auth_view.LoginView.as_view(
            template_name='authentication_login.html',
            authentication_form=LoginForm), name='login'),
    path(
        'logout',
        auth_view.LogoutView.as_view(next_page="login"),
        name='logout'),
    path('registration', RegistrationView.as_view(success_url=reverse_lazy("base"), form_class=RegistrationCustomForm,
                                                  template_name='registration.html'),
         name='register'),
    path('lk', views.lk, name='lk'),
    path('user-lk', views.user_lk, name='user_lk'),
    path('admin-lk', views.AdminLk.as_view(), name='admin_lk'),
    path('admin-lk/attendance/yes/<int:classes_id>', views.attendance_true, name='attendance_true'),
    path('admin-lk/attendance/no/<int:classes_id>', views.attendance_false, name='attendance_false'),
    path('employee/<int:user_id>', views.employee_info, name='employee_info'),
    path('employee/all', views.employee_list, name='employee_list'),
    path('faq-all', views.faq_list, name='faq_list'),
    path('faq/<int:faq_id>', views.faq_answer, name='faq_answer'),
    path('manager-lk', views.manager_lk_view, name='manager_lk'),
    path('partner-lk', views.partner_lk_view, name='partner_lk'),
    path('partner/new', views.create_partner_view, name='create_partner'),
    path('partner/edit/<int:user_id>', views.edit_partner_view, name='edit_partner'),
    path('employee/new', views.create_employee_view, name='create_employee'),
    path('employee/edit/<int:user_id>', views.edit_employee_view, name='edit_employee'),
    path(
        'request/new', views.form_request_view, name='form_request'),
    path(
        'review/new', views.feedback_form_view, name='form_review'),
    path('shop/new', views.shop_form_view, name='shop_form'),
    path('notification', views.notification_view, name='notification'),
    path(
        'shop/<int:shop_id>',
        login_required(views.ShopListView.as_view()),
        name='shop'),
    path(
        'task/new/<int:partner_id>', views.form_task_view, name='form_task'),
    path(
        'task/<int:task_id>-<int:user_id>', views.task_view, name='task'),
    path(
        'request/<int:requests_id>-<int:user_id>', views.requests_view, name='request'),
    path(
        'review/<int:feedback_id>-<int:user_id>', views.feedback_view, name='feedback'),
    path('load/request', views.load_filtered_request, name='load_filtered_request'),
    path('load/feedback-shop/<int:shop_id>', views.load_filtered_shop_feedback, name='load_filtered_shop_feedback'),
    path('load/feedback', views.load_filtered_feedback, name='load_filtered_feedback'),
    path('load/tasks', views.load_filtered_tasks, name='load_filtered_tasks'),
    path('load/idea', views.load_filtered_idea, name='load_filtered_ideas'),
    path('load/events', views.load_filtered_events, name='load_filtered_events'),
    path('load/calendar', views.load_filtered_calendar, name='load_filtered_calendar'),
    path('load_paginations_docs', views.load_paginations_docs, name='load_paginations_docs'),
    path('load_docs', views.load_docs, name='load_docs'),
    path('ya_kassa/<int:classes_id>', views.ya_kassa, name='ya_kassa'),
    path('api/ya_kassa_notification', YaKassaNotify.as_view(), name='ya_kassa_notification')
]
