from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from wagtail.documents.forms import get_document_form

from mickroservices.models import DocumentSushi, Subjects
from mickroservices.models import CourseModel, ScheduleModel
from mickroservices.forms import ScheduleForm
from mickroservices.views.tech_cards import SushiDocListView


def get_documents(doc_type):
    documents = DocumentSushi.objects.filter(doc_type=doc_type)
    return documents

class CoursesView(SushiDocListView):
    template_name = 'lessons.html'
    model = CourseModel
    document_model = DocumentSushi
    paginate_by = 10
    doc_type = DocumentSushi.T_TRAINING

    def get_context_data(self, **kwargs):
        context = super(CoursesView, self).get_context_data(**kwargs)
        context['breadcrumb'] = [{'title': 'Обучение'}]
        subjects = Subjects.objects.filter(type= DocumentSushi.T_TRAINING)
        context['subjects'] = subjects
        context['doc_type'] = DocumentSushi.T_TRAINING
        context['documents'] = self.documents
        return context

    def get_queryset(self):

        # Get documents (filtered by user permission)
        self.documents = super().get_queryset()
        return self.model.objects.all()

class CourseView(DetailView):
    template_name = 'schedule.html'
    model = CourseModel


class ScheduleListView(ListView):
    template_name = 'schedule.html'
    model = ScheduleModel
    paginate_by = 10
    context_object_name = 'schedule_list'

    def get_context_data(self, **kwargs):
        context = super(ScheduleListView, self).get_context_data(**kwargs)

        context['breadcrumb'] = [
            {'title': 'Обучение',
             'url': reverse_lazy('mickroservices:lessons')},
            {'title': 'Расписание'}
        ]
        return context


class ScheduleView(UpdateView):
    template_name = 'schedule_form.html'
    form_class = ScheduleForm
    model = ScheduleModel
    success_url = reverse_lazy('mickroservices:schedule')

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        context['title'] = 'Редактировать расписание'
        context['breadcrumb'] = [
            {'title': 'Обучение',
             'url': reverse_lazy('mickroservices:lessons')},
            {'title': 'Расписание',
             'url': reverse_lazy('mickroservices:schedule')},
            {'title': context['title']}
        ]
        return context

    def form_invalid(self, form, ms='Ошибка заполнения формы'):
        print(form.errors)
        return TemplateResponse(self.request, self.template_name,
                                {'form': form,
                                 'status_ms': True,
                                 'message': ms})


class ScheduleCreateView(CreateView):
    template_name = 'schedule_form.html'
    form_class = ScheduleForm
    success_url = reverse_lazy('mickroservices:schedule')

    def get_context_data(self, **kwargs):
        context = super(ScheduleCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить расписание'
        context['breadcrumb'] = [
            {'title': 'Обучение',
             'url': reverse_lazy('mickroservices:lessons')},
            {'title': 'Расписание',
             'url': reverse_lazy('mickroservices:schedule')},
            {'title': context['title']}
        ]
        return context

    def form_invalid(self, form, ms='Ошибка заполнения формы'):
        print(form.errors)
        print(form.cleaned_data)
        return TemplateResponse(self.request, self.template_name,
                                {'form': form,
                                 'status_ms': True,
                                 'message': ms})
