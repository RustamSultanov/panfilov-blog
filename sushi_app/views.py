from calendar import Calendar, nextmonth
from datetime import date, datetime, timedelta

import uuid
import wagtail.users.models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import modelformset_factory
from django.forms.models import model_to_dict
from django.http import (
    HttpResponseBadRequest, JsonResponse, HttpResponseRedirect, HttpResponse)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_text
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView
from ls.joyous.models import getAllEventsByDay, RecurringEventPage
from psycopg2._range import DateTimeTZRange
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.auth import user_passes_test
from wagtail.core.models import Collection
from wagtail.documents.forms import get_document_form
from wagtail.documents.permissions import permission_policy
from wagtail.users.forms import AvatarPreferencesForm
from yandex_checkout import Configuration, Payment
from yandex_checkout.domain.common.user_agent import Version

from chat.models import Message as Chat_Message
from mickroservices.forms import AnswerForm, IdeaStatusForm
from mickroservices.models import NewsPage, QuestionModel, IdeaModel
from .forms import *
from .models import *
import environ

env = environ.Env(DEBUG=(bool, False), )
# reading .env file
environ.Env.read_env()

User = get_user_model()


def get_filtered_shop_feedback(request, shop_id):
    feedback_list = Feedback.objects.prefetch_related("responsible", "shop").filter(
        shop=shop_id
    )
    if "filter_feedback" in request.GET:
        return feedback_list.filter(status=request.GET['filter_feedback'])
    return feedback_list


@csrf_exempt
def load_filtered_shop_feedback(request, shop_id):
    feedback_list = get_filtered_shop_feedback(request, shop_id)
    return render(
        request,
        'partials/feedback_manager.html',
        {'feedback_list': feedback_list}
    )


class ShopListView(ListView):
    model = DocumentSushi
    paginate_by = 9
    context_object_name = "documents"
    template_name = "store.html"

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["shop_id"])
        context = super().get_context_data(**kwargs)
        context["invoices"] = self.get_invoices()
        context["shop"] = shop
        context["feedback_list"] = get_filtered_shop_feedback(self.request, self.kwargs["shop_id"])
        context["doc_type"] = DocumentSushi.T_PERSONAL
        context["type_invoice"] = DocumentSushi.T_PERSONAL_INVOICES
        context["breadcrumb"] = [
            {"title": "Личный кабинет", "url": reverse_lazy("partner_lk")},
            {"title": f"Магазин #{shop.id}"},
        ]
        return context

    def get_documents(self):
        shop = Shop.objects.get(id=self.kwargs["shop_id"])
        documents = shop.docs.all().order_by("title")
        return documents

    def get_invoices(self):
        shop = Shop.objects.get(id=self.kwargs["shop_id"])
        return shop.checks.all().order_by("title")

    def get_queryset(self):
        # Get documents (filtered by user permission)
        documents = self.get_documents()
        invoices = self.get_invoices()
        # Ordering

        ordering = None
        if "ordering" in self.request.GET and self.request.GET["ordering"] in [
            "title",
            "-created_at",
            "file_size",
        ]:
            ordering = self.request.GET["ordering"]
        else:
            ordering = "title"

        documents = documents.order_by(ordering)
        # Search
        query_string = None
        if "q" in self.request.GET:
            form = SearchForm(self.request.GET, placeholder="Search documents")
            if form.is_valid():
                query_string = form.cleaned_data["q"]
                documents = documents.search(query_string)

        return documents

    def get(self, request, *args, **kwargs):
        collections = permission_policy.collections_user_has_any_permission_for(
            request.user, ["add", "change"]
        )
        if len(collections) < 2:
            collections = None
        else:
            collections = Collection.order_for_display(collections)

        # Create response
        return super().get(request, *args, **kwargs)

    def verife_http_response(self, request):
        if not request.is_ajax():
            return HttpResponseBadRequest("Cannot POST to this view without AJAX")

        if not request.FILES:
            return HttpResponseBadRequest("Must upload a file")
        return None

    def get_doc_form(self, request):
        # Build a form for validation
        DocumentForm = get_document_form(self.model)
        return DocumentForm(
            {
                "title": request.FILES["file"].name,
                "collection": request.POST.get("collection"),
            },
            {"file": request.FILES["file"]},
            user=request.user,
        )

    def save_doc(self, request, doc, doc_type):
        doc.doc_type = doc_type
        doc.uploaded_by_user = request.user
        doc.file_size = doc.file.size

        # Set new document file hash
        doc.file.seek(0)
        doc._set_file_hash(doc.file.read())
        doc.file.seek(0)
        doc.save()

    @vary_on_headers("X-Requested-With")
    def post(self, request, *args, **kwargs):

        respone = self.verife_http_response(request)
        if respone:
            return respone

        form = self.get_doc_form(request)

        if form.is_valid():
            # Save it
            doc = form.save(commit=False)

            doc_type = DocumentSushi.T_PERSONAL_INVOICES \
                if request.POST.get("type") == "invoice" else DocumentSushi.T_PERSONAL

            self.save_doc(request, doc, doc_type)

            shop = Shop.objects.get(id=self.kwargs["shop_id"])

            if request.POST.get("type") == "doc":
                shop.docs.add(doc)
            elif request.POST.get("type") == "invoice":
                shop.checks.add(doc)
            return JsonResponse({"success": True})
        else:
            # Validation error
            return JsonResponse(
                {
                    "success": False,
                    "error_message": "\n".join(
                        [
                            "\n".join([force_text(i) for i in v])
                            for k, v in form.errors.items()
                        ]
                    ),
                }
            )


# # Create your views here
def manager_check(user):
    return user.user_profile.is_manager


def partner_check(user):
    return user.user_profile.is_partner


def head_check(user):
    return user.user_profile.is_head


def admin_check(user):
    return user.is_superuser


def base(request):
    employees_list = UserProfile.objects.prefetch_related(
        "user", "wagtail_profile", "department"
    ).all()
    news_all = NewsPage.objects.all().order_by(
        'first_published_at')
    if len(news_all) == 0 or len(news_all) == 1 or len(news_all) == 2 or len(news_all) == 3:
        news = news_all
    else:
        news = news_all[len(news_all) - 3:]
    today = timezone.localdate()
    c = Calendar()
    dates = list(c.itermonthdays3(today.year, today.month))
    date_select = date(today.year, today.month, today.day)
    ev = getAllEventsByDay(request, date_select, date_select)
    rec_pages = [r for r in ev[0].days_events if
                 len(Classes.objects.filter(recurrences_event=r.page, is_busy=True, duration=DateTimeTZRange(
                     lower=date_select + timedelta(minutes=r.page.time_from.minute, hours=r.page.time_from.hour - 3),
                     upper=date_select + timedelta(minutes=r.page.time_to.minute,
                                                   hours=r.page.time_to.hour - 3)))) == 0]
    form = EventForm(request.POST or None, lst_events=rec_pages)
    if form.is_valid():
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("login"))
        rev = RecurringEventPage.objects.get(id=int(form.data['events']))
        dt = datetime.strptime(form.data['date'], "%d.%m.%Y")
        cl_ev = Classes(date_lessons=dt + timedelta(minutes=rev.time_from.minute, hours=rev.time_from.hour),
                        user=request.user, is_busy=True, duration=DateTimeTZRange(
                lower=dt + timedelta(minutes=rev.time_from.minute, hours=rev.time_from.hour - 3),
                upper=dt + timedelta(minutes=rev.time_to.minute, hours=rev.time_to.hour - 3)), recurrences_event=rev)
        cl_ev.save()
        return HttpResponseRedirect(reverse_lazy("ya_kassa"))
    return render(request, "index.html", {"employee_list": employees_list, "news": news,
                                          'calendar': [dates[i:i + 7] for i in range(0, len(dates), 7)],
                                          'today': today, 'form': form})


@login_required
def user_lk(request):
    classes_list = Classes.objects.filter(user=request.user)
    return render(
        request,
        "account.html",
        {"classes_list": classes_list,
         "breadcrumb": [{"title": "Личный кабинет"}],

         },
    )


class AdminLk(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'attendance.html'
    model = Classes
    paginate_by = 9
    context_object_name = 'classes_list'
    ordering = '-date_create'

    def get_context_data(self, **kwargs):
        context = super(AdminLk, self).get_context_data(**kwargs)
        context['breadcrumb'] = [{"title": "Личный кабинет"}]
        return context

    def test_func(self):
        return self.request.user.is_superuser


@login_required
@user_passes_test(admin_check)
def attendance_true(request, classes_id):
    classes = get_object_or_404(Classes, id=classes_id)
    classes.is_attended = True
    classes.is_not_attended = False
    classes.save()
    return HttpResponseRedirect(reverse_lazy("admin_lk"))


@login_required
@user_passes_test(admin_check)
def attendance_false(request, classes_id):
    classes = get_object_or_404(Classes, id=classes_id)
    classes.is_attended = False
    classes.is_not_attended = True
    classes.save()
    return HttpResponseRedirect(reverse_lazy("admin_lk"))


@login_required
def lk(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse_lazy("admin_lk"))
    else:
        return HttpResponseRedirect(reverse_lazy("user_lk"))


@login_required
def employee_list(request):
    today = timezone.localdate()
    e = [i.days_events for i in getAllEventsByDay(request, date(2020, 5, 10), date(2020, 5, 10))]
    # ew = [i.days_events for i in getAllEventsByWeek(request,today.year,today.month)]
    c = Calendar()
    cc = [(year, month, day, day_of_week) for year, month, day, day_of_week in
          c.itermonthdays4(today.year, today.month)]
    return HttpResponse(f"{e}")


def get_calendar(request):
    if "filter_month" in request.GET:
        today = timezone.localdate()
        nx_mth = nextmonth(today.year, today.month)
        date_next = date(nx_mth[0], nx_mth[1], 1)
        td = today if today.month == int(request.GET['filter_month']) else date_next
        c = Calendar()
        dates = list(c.itermonthdays3(int(request.GET['filter_year']), int(request.GET['filter_month'])))
        return ([dates[i:i + 7] for i in range(0, len(dates), 7)], td)


def get_filtered_events(request):
    if "filter_date" in request.GET:
        date_select = date(int(request.GET['filter_year']), int(request.GET['filter_month']),
                           int(request.GET['filter_date']))
        ev = getAllEventsByDay(request, date_select, date_select)
        rec_pages = list()

        for r in ev[0].days_events:
            dt = datetime(int(request.GET['filter_year']), int(request.GET['filter_month']),
                          int(request.GET['filter_date'])) + timedelta(
                minutes=r.page.time_from.minute,
                hours=r.page.time_from.hour)
            cl_lst = Classes.objects.filter(recurrences_event=r.page, is_busy=True,
                                            date_lessons=dt)
            if len(cl_lst) == 0:
                rec_pages.append(r)
        form = EventForm(request.POST or None, lst_events=rec_pages)
        return form


@login_required
def employee_info(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "employee.html", {"employee": user})


@login_required
def notification_view(request):
    notifications = Chat_Message.objects.select_related("sender", "task", "requests", "feedback", "idea",
                                                        "question").filter(recipient=request.user).order_by(
        '-created_at')
    paginator = Paginator(notifications, 10)
    page = request.GET.get('page')
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)
    is_paginated = paginator.num_pages > 1
    return render(request, "notifications.html",
                  {"notifications": notifications, "is_paginated": is_paginated, "breadcrumb": [
                      {"title": "Оповещения"},
                  ]})


def get_filtered_tasks(request):
    ''' Возвращает список задачи сотрудника
        Если присутсвует GET параметр 'filter_task', то
        применяется фильтрация
    '''
    if request.user.user_profile.is_manager:
        tasks = Task.objects.prefetch_related("responsible") \
            .filter(manager=request.user.user_profile)
    else:
        tasks = Task.objects.prefetch_related("responsible") \
            .filter(responsible=request.user)
    if "filter_task" in request.GET:
        return tasks.filter(status=request.GET['filter_task'])
    return tasks


def get_filtered_request(request):
    if request.user.user_profile.is_manager:
        request_list = Requests.objects.prefetch_related("responsible").filter(
            manager=request.user.user_profile
        )
    else:
        request_list = Requests.objects.prefetch_related("responsible") \
            .filter(responsible=request.user)
    if "filter_request" in request.GET:
        return request_list.filter(status=request.GET['filter_request'])
    return request_list.order_by("-date_create")


def get_filtered_feedback(request):
    if request.user.user_profile.is_manager:
        feedback_list = Feedback.objects.prefetch_related("responsible", "shop").filter(
            manager=request.user.user_profile
        )
    else:
        feedback_list = Feedback.objects.prefetch_related("responsible", "shop").filter(
            responsible=request.user.user_profile
        )
    if "filter_feedback" in request.GET:
        return feedback_list.filter(status=request.GET['filter_feedback'])
    return feedback_list.order_by("-date_create")


def get_filtered_idea(request):
    StatusFormSet = modelformset_factory(IdeaModel, form=IdeaStatusForm, extra=0)
    formset = StatusFormSet(request.POST or None, queryset=IdeaModel.objects.filter(recipient=request.user),
                            prefix='idea')
    if request.user.user_profile.is_manager:
        idea_list = IdeaModel.objects.select_related("sender", "recipient").filter(
            recipient=request.user
        )
    else:
        idea_list = IdeaModel.objects.select_related("sender", "recipient").filter(
            sender=request.user
        )
    if "filter_idea" in request.GET:
        return (idea_list.filter(status=request.GET['filter_idea']), StatusFormSet(request.POST or None,
                                                                                   queryset=IdeaModel.objects.filter(
                                                                                       recipient=request.user,
                                                                                       status=request.GET[
                                                                                           'filter_idea']),
                                                                                   prefix='idea'))
    return (idea_list, formset)


@login_required
@user_passes_test(manager_check)
def faq_list(request):
    faq_all = QuestionModel.objects.all()
    return render(request, "faq_list.html", {"faq_all": faq_all})


@login_required
@user_passes_test(manager_check)
def faq_answer(request, faq_id):
    question = get_object_or_404(QuestionModel, id=faq_id)
    form = AnswerForm(request.POST or None, instance=question)
    if form.is_valid():
        new_q = form.save(commit=False)
        new_q.status = QuestionModel.ST_REJECTED if new_q.hide else QuestionModel.ST_OK
        new_q.save()
        Chat_Message.objects.create(
            sender=request.user,
            recipient=question.user,
            body=f"Дан ответ на вопрос {new_q.theme}",
            question=question
        )
        return HttpResponseRedirect(reverse_lazy("faq_list"))
    return render(
        request,
        "faq_answer.html",
        {
            "question": question,
            "form": form,
            "breadcrumb": [
                {"title": "Список вопросов", "url": reverse_lazy("faq_list")},
                {"title": "Добавить ответ"},
            ],
        },
    )


@login_required
@user_passes_test(manager_check)
def manager_lk_view(request):
    partner_list = UserProfile.objects.prefetch_related(
        "user", "wagtail_profile"
    ).filter(manager=request.user.user_profile)
    task_not_solved = Task.objects.filter(status=ST_IN_PROGRESS,
                                          manager=request.user.user_profile).count()
    requests_not_solved = Requests.objects.filter(status=ST_IN_PROGRESS,
                                                  manager=request.user.user_profile).count()
    ideas_not_solved = IdeaModel.objects.filter(status=IdeaModel.ST_CONSIDERATION,
                                                recipient=request.user).count()
    feedback_not_solved = Feedback.objects.filter(status=Feedback.ST_NOT_SOLVED,
                                                  manager=request.user.user_profile).count()
    request_list = get_filtered_request(request)
    task_list = get_filtered_tasks(request)
    feedback_list = get_filtered_feedback(request)
    page_object = Paginator(DocumentSushi.objects.all(), 9)
    is_paginated = False
    page = request.GET['page'] if 'page' in request.GET else 1
    page_obj = documents = page_object.get_page(page)
    data = get_filtered_idea(request)
    idea_list = data[0]
    formset = data[1]
    if formset.is_valid():
        formset.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') + "#ideas")
    return render(
        request,
        "dashboard_manager.html",
        {
            'idea_list': idea_list,
            'formset': formset,
            "partner_list": partner_list,
            "request_list": request_list,
            "task_list": task_list,
            "task_not_solved": task_not_solved,
            "ideas_not_solved": ideas_not_solved,
            "requests_not_solved": requests_not_solved,
            "feedback_not_solved": feedback_not_solved,
            "feedback_list": feedback_list,
            "breadcrumb": [{"title": "Личный кабинет"}],
            "documents": documents,
            "page_obj": page_obj,
            "is_paginated": is_paginated

        },
    )


@csrf_exempt
def load_filtered_idea(request):
    data = get_filtered_idea(request)
    idea_list = data[0]
    formset = data[1]
    return render(
        request,
        'partials/ideas_manager.html',
        {'idea_list': idea_list, 'formset': formset}
    )


@csrf_exempt
def load_filtered_calendar(request):
    dates, today = get_calendar(request)
    return render(
        request,
        'partials/calendar.html',
        {'calendar': dates, 'today': today}
    )


@csrf_exempt
def load_filtered_events(request):
    form = get_filtered_events(request)
    return render(
        request,
        'partials/events.html',
        {'form': form}
    )


@csrf_exempt
def load_filtered_tasks(request):
    task_list = get_filtered_tasks(request)
    return render(
        request,
        'partials/tasks_manager.html',
        {'task_list': task_list}
    )


@csrf_exempt
def load_filtered_request(request):
    request_list = get_filtered_request(request)
    return render(
        request,
        'partials/request_manager.html',
        {'request_list': request_list}
    )


@csrf_exempt
def load_filtered_feedback(request):
    feedback_list = get_filtered_feedback(request)
    return render(
        request,
        'partials/feedback_manager.html',
        {'feedback_list': feedback_list}
    )


@csrf_exempt
def load_docs(request):
    if 'doc_type' in request.GET:
        docs = DocumentSushi.objects.filter(doc_type=request.GET['doc_type'])
    else:
        docs = []

    if docs and 'sub_type' in request.GET:
        docs = DocumentSushi.objects.filter(sub_type=request.GET['sub_type'])
    return render(
        request,
        'partials/documents.html',
        {'documents': docs}
    )


@csrf_exempt
def load_paginations_docs(request):
    if 'doc_type' in request.GET:
        docs = DocumentSushi.objects.filter(doc_type=request.GET['doc_type'])
    else:
        docs = []

    if docs and 'sub_type' in request.GET:
        docs = docs.filter(sub_type=request.GET['sub_type'])
        print("=====================================================")
        print(docs[0], docs[0].sub_type)

    page_object = Paginator(docs, 9)
    return render(
        request,
        'partials/pagination.html',
        {'posts': page_object.get_page(1)}
    )


@login_required
@user_passes_test(partner_check)
def partner_lk_view(request):
    shop_list = Shop.objects.prefetch_related("checks", "docs").filter(
        partner=request.user.user_profile
    )
    task_not_solved = Task.objects.filter(status=ST_IN_PROGRESS,
                                          responsible=request.user).count()
    feedback_not_solved = Feedback.objects.filter(status=Feedback.ST_NOT_SOLVED,
                                                  responsible=request.user.user_profile).count()
    requests_not_solved = Requests.objects.filter(status=ST_IN_PROGRESS,
                                                  responsible=request.user).count()
    request_list = get_filtered_request(request)
    task_list = get_filtered_tasks(request)
    feedback_list = get_filtered_feedback(request)
    documents = DocumentSushi.objects.all()
    page_object = Paginator(documents, 9)
    is_paginated = False
    page_obj = documents = []
    if page_object.num_pages > 0:
        is_paginated = True
        page = request.GET['page'] if 'page' in request.GET else 1
        page_obj = documents = page_object.get_page(page)

    return render(
        request,
        "dashboard_partner.html",
        {
            "shop_list": shop_list,
            "request_list": request_list,
            "task_list": task_list,
            "feedback_not_solved": feedback_not_solved,
            "task_not_solved": task_not_solved,
            "requests_not_solved": requests_not_solved,
            "feedback_list": feedback_list,
            "breadcrumb": [{"title": "Личный кабинет"}],
            "manager": request.user.user_profile.manager,
            "documents": documents,
            "page_obj": page_obj,
            "is_paginated": is_paginated
        },
    )


@login_required
@user_passes_test(partner_check)
def form_request_view(request):
    form = RequestsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.responsible = request.user
        form.manager = request.user.user_profile.manager
        form.save()
        Chat_Message.objects.create(
            sender=request.user,
            recipient=request.user.user_profile.manager.user,
            body="Создан запрос",
            requests=form
        )
        return HttpResponseRedirect(reverse_lazy("partner_lk"))
    return render(
        request,
        "request_new.html",
        {
            "manager": request.user.user_profile.manager,
            "form": form,
            "breadcrumb": [
                {"title": "Личный кабинет", "url": reverse_lazy("partner_lk")},
                {"title": "Добавить задачу"},
            ],
        },
    )


@login_required
@user_passes_test(manager_check)
def form_task_view(request, partner_id):
    partner = get_object_or_404(UserProfile, id=partner_id)
    form = TaskForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.responsible = partner.user
        form.manager = request.user.user_profile
        form.save()
        Chat_Message.objects.create(
            sender=request.user,
            recipient=partner.user,
            body=f"Создана задача от {request.user.get_full_name()}",
            task=form
        )
        return HttpResponseRedirect(reverse_lazy("manager_lk"))
    return render(
        request,
        "task_new.html",
        {
            "partner": partner,
            "form": form,
            "breadcrumb": [
                {
                    "title": partner.user.get_full_name,
                    "url": reverse("employee_info", args=[partner.user.id]),
                },
                {"title": "Добавить задачу"},
            ],
        },
    )


@login_required
@user_passes_test(manager_check)
def feedback_form_view(request):
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.responsible = form.shop.partner
        form.manager = request.user.user_profile
        form.save()
        Chat_Message.objects.create(
            sender=request.user,
            recipient=form.shop.partner.user,
            body=f"Создан отзыв на магазин {form.shop}",
            feedback=form
        )
        return HttpResponseRedirect(reverse_lazy("manager_lk"))
    context = {
        "form": form,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Добавить отзыв"},
        ],
    }
    return render(request, "review_new.html", context)


@login_required
@user_passes_test(manager_check)
def create_partner_view(request):
    form_user = RegistrationEmployeeMainForm(
        request.POST or None, request.FILES or None, prefix="user"
    )
    form_user_profile = RegistrationPartnerAdditionForm(
        request.POST or None, request.FILES or None, prefix="user_profile"
    )
    if form_user.is_valid() and form_user_profile.is_valid():
        form_user = form_user.save(commit=False)
        form_user.set_password(form_user.password)
        form_user.save()
        editor_group = Group.objects.get(name='Editors')
        form_user.groups.add(editor_group)
        wagtail_user = wagtail.users.models.UserProfile.get_for_user(form_user)
        wagtail_user.avatar = form_user_profile.cleaned_data["avatar"]
        wagtail_user.preferred_language = settings.LANGUAGE_CODE
        wagtail_user.current_time_zone = settings.TIME_ZONE
        wagtail_user.save()
        form_user_profile = form_user_profile.save(commit=False)
        form_user_profile.user = form_user
        form_user_profile.wagtail_profile = wagtail_user
        form_user_profile.manager = request.user.user_profile
        form_user_profile.is_partner = True
        form_user_profile.save()
        return HttpResponseRedirect(reverse("employee_info", args=[form_user.id]))
    context = {
        "form_user": form_user,
        "form_user_profile": form_user_profile,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Добавить франчайзи"},
        ],
    }
    return render(request, "user_new.html", context)


@login_required
@user_passes_test(manager_check)
def edit_partner_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form_user = EditEmployeeMainForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user),
        instance=user,
        prefix="user",
    )
    form_user_profile = EditPartnerAdditionForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user.user_profile),
        instance=user.user_profile,
        prefix="user_profile",
    )
    form_wagtail = AvatarPreferencesForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user.wagtail_userprofile),
        instance=user.wagtail_userprofile,
        prefix="user_profile",
    )
    if (
            form_user.is_valid()
            and form_user_profile.is_valid()
            and form_wagtail.is_valid()
    ):
        form_user.save()
        form_user_profile.save()
        form_wagtail.save()
        return HttpResponseRedirect(reverse("employee_info", args=[user_id]))
    context = {
        "form_user": form_user,
        "form_user_profile": form_user_profile,
        "form_wagtail": form_wagtail,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Редактировать франчайзи"},
        ],
    }
    return render(request, "user_edit.html", context)


@login_required
@user_passes_test(head_check)
def create_employee_view(request):
    form_user = RegistrationEmployeeMainForm(
        request.POST or None, request.FILES or None, prefix="user"
    )
    form_user_profile = RegistrationEmployeeAdditionForm(
        request.POST or None, request.FILES or None, prefix="user_profile"
    )
    if form_user.is_valid() and form_user_profile.is_valid():
        form_user = form_user.save(commit=False)
        form_user.set_password(form_user.password)
        form_user.save()
        editor_group = Group.objects.get(name='Editors')
        form_user.groups.add(editor_group)
        wagtail_user = wagtail.users.models.UserProfile.get_for_user(form_user)
        wagtail_user.avatar = form_user_profile.cleaned_data["avatar"]
        wagtail_user.preferred_language = settings.LANGUAGE_CODE
        wagtail_user.current_time_zone = settings.TIME_ZONE
        wagtail_user.save()
        form_user_profile = form_user_profile.save(commit=False)
        form_user_profile.user = form_user
        form_user_profile.wagtail_profile = wagtail_user
        form_user_profile.head = request.user.user_profile
        form_user_profile.is_manager = True
        form_user_profile.save()
        return HttpResponseRedirect(reverse("employee_info", args=[form_user.id]))
    context = {
        "form_user": form_user,
        "form_user_profile": form_user_profile,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Добавить сотрудника"},
        ],
    }
    return render(request, "employee_new.html", context)


@login_required
def edit_employee_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        if request.user.user_profile.is_partner:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    form_user = EditEmployeeMainForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user),
        instance=user,
        prefix="user",
    )
    form_user_profile = EditEmployeeAdditionForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user.user_profile),
        instance=user.user_profile,
        prefix="user_profile",
    )
    form_wagtail = AvatarPreferencesForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user.wagtail_userprofile),
        instance=user.wagtail_userprofile,
        prefix="user_profile",
    )
    if (
            form_user.is_valid()
            and form_user_profile.is_valid()
            and form_wagtail.is_valid()
    ):
        form_user.save()
        form_user_profile.save()
        form_wagtail.save()
        return HttpResponseRedirect(reverse("employee_info", args=[user_id]))
    context = {
        "form_user": form_user,
        "form_user_profile": form_user_profile,
        "form_wagtail": form_wagtail,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Редактировать сотрудника"},
        ],
    }
    return render(request, "employee_edit.html", context)


@login_required
@user_passes_test(manager_check)
def shop_form_view(request):
    form = ShopForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.save()
        return HttpResponseRedirect(reverse_lazy("shop", args=[form.id]))
    context = {
        "form": form,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Добавить магазин"},
        ],
    }
    return render(request, "store_new.html", context)


# @login_required
# def shop_view(request, shop_id):
#     shop = get_object_or_404(Shop, id=shop_id)
#     return render(request, 'store.html', {'shop': shop,
#                                           'breadcrumb': [{'title': 'Личный кабинет',
#                                                           'url': reverse_lazy('partner_lk')},
#                                                          {'title': f"Магазин #{shop.id}"}]})


@login_required
def task_view(request, task_id, user_id):
    task = get_object_or_404(Task, id=task_id)
    if task.responsible != request.user:
        if task.manager != request.user.user_profile:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    form_status = StatusTaskForm(
        request.POST or None, initial=model_to_dict(task), instance=task
    )
    if request.user.user_profile.is_manager:
        if form_status.is_valid():
            new_status = form_status.save(commit=False)
            if new_status.status == ST_SOLVED:
                Chat_Message.objects.create(
                    sender=request.user,
                    recipient=task.responsible,
                    body="Задача переведена в статус решена",
                    task=new_status
                )
            new_status.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    qs1 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        task=task, from_user=request.user.id
    )
    qs2 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        task=task, to_user=request.user.id
    )
    messeges = qs1.union(qs2).order_by("date_create")
    form = MessegesFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        task_new = form.save(commit=False)
        task_new.task = task
        task_new.from_user = request.user
        if request.user == task.responsible:
            task_new.to_user = task.manager.user
        else:
            task_new.to_user = task.responsible
        task_new.save()
        Chat_Message.objects.create(
            sender=task_new.from_user,
            recipient=task_new.to_user,
            body=task_new.text,
            task=task
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#coments")
    return render(
        request,
        "task.html",
        {
            "task": task,
            "messeges": messeges,
            "form": form,
            "form_status": form_status,
            "breadcrumb": [
                {
                    "title": "Личный кабинет",
                    "url": reverse_lazy("partner_lk")
                    if request.user.user_profile.is_partner
                    else reverse_lazy("manager_lk"),
                },
                {"title": f"Задача #{task.id}"},
            ],
        },
    )


@login_required
def requests_view(request, requests_id, user_id):
    requests = get_object_or_404(Requests, id=requests_id)
    if requests.responsible != request.user:
        if requests.manager != request.user.user_profile:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    form_status = StatusRequestsForm(
        request.POST or None, initial=model_to_dict(requests), instance=requests
    )
    if request.user.user_profile.is_manager:
        if form_status.is_valid():
            form_status.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    qs1 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        requests=requests, from_user=request.user.id
    )
    qs2 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        requests=requests, to_user=request.user.id
    )
    messeges = qs1.union(qs2).order_by("date_create")
    form = MessegesFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.requests = requests
        form.from_user = request.user
        if request.user == requests.responsible:
            form.to_user = requests.manager.user
        else:
            form.to_user = requests.responsible
        form.save()
        Chat_Message.objects.create(
            sender=form.from_user,
            recipient=form.to_user,
            body=form.text,
            requests=requests
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#coments")
    return render(
        request,
        "request.html",
        {
            "requests": requests,
            "messeges": messeges,
            "form": form,
            "form_status": form_status,
            "breadcrumb": [
                {
                    "title": "Личный кабинет",
                    "url": reverse_lazy("partner_lk")
                    if request.user.user_profile.is_partner
                    else reverse_lazy("manager_lk"),
                },
                {"title": f"Запрос #{requests.id}"},
            ],
        },
    )


@login_required
def feedback_view(request, feedback_id, user_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if feedback.responsible != request.user.user_profile:
        if feedback.manager != request.user.user_profile:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    form_status = StatusFeedbackForm(
        request.POST or None, initial=model_to_dict(feedback), instance=feedback
    )
    if form_status.is_valid():
        form_status.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    qs1 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        feedback=feedback, from_user=request.user.id
    )
    qs2 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        feedback=feedback, to_user=request.user.id
    )
    messeges = qs1.union(qs2).order_by("date_create")
    form = MessegesFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.feedback = feedback
        form.from_user = request.user
        if request.user == feedback.responsible.user:
            form.to_user = feedback.manager.user
        else:
            form.to_user = feedback.responsible.user
        form.save()
        Chat_Message.objects.create(
            sender=form.from_user,
            recipient=form.to_user,
            body=form.text,
            feedback=feedback
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#coments")
    return render(
        request,
        "review.html",
        {
            "feedback": feedback,
            "messeges": messeges,
            "form": form,
            "form_status": form_status,
            "breadcrumb": [
                {
                    "title": "Личный кабинет",
                    "url": reverse_lazy("partner_lk")
                    if request.user.user_profile.is_partner
                    else reverse_lazy("manager_lk"),
                },
                {"title": f"Отзыв #{feedback.id}"},
            ],
        },
    )


@login_required
def ya_kassa(request, classes_id):
    classes = get_object_or_404(Classes, id=classes_id)
    if classes.user != request.user:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    Configuration.configure(env('YA_KASSA_CLIENT_ID'), env('YA_KASSA_SECRET_KEY'))
    Configuration.configure_user_agent(
        framework=Version('Django', '2.2.3'),
        cms=Version('Wagtail', '2.6.2')
    )
    payment = Payment.create({
        "amount": {
            "value": f"{classes.cost}.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://xn--80aaah3ajhdqggh1e5b.xn--p1ai/user-lk"
        },
        "capture": True,
        "description": f"Заказ №{classes.id}"
    }, uuid.uuid4())
    classes.pay_id = payment.id
    classes.save()
    return HttpResponseRedirect(payment.confirmation.confirmation_url)


class YaKassaNotify(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        p_id = request.data['object']['id']
        classes = get_object_or_404(Classes, pay_id=p_id)
        if request.data['object']['status'] == 'succeeded':
            classes.is_paid = True
            classes.save()
        else:
            classes.delete()
        return Response(status=200)
