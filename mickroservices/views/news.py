from django.template.response import TemplateResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.http import HttpResponseRedirect

from mickroservices.models import NewsPage, Blog
from mickroservices.forms import NewsForm
from wagtail.core.models import Page


class BlogsView(ListView):
    template_name = 'blogs.html'
    model = Blog
    paginate_by = 9
    context_object_name = 'news'
    ordering = 'first_published_at'

    def get_context_data(self, **kwargs):
        context = super(BlogsView, self).get_context_data(**kwargs)
        context['breadcrumb'] = [{'title': 'Блог'}]
        return context


class NewsView(ListView):
    template_name = 'news.html'
    model = NewsPage
    paginate_by = 9
    context_object_name = 'news'
    ordering = 'first_published_at'

    def get_context_data(self, **kwargs):
        context = super(NewsView, self).get_context_data(**kwargs)
        context['breadcrumb'] = [{'title': 'Программы'}]
        return context


class NewsCreateView(CreateView):
    template_name = 'news_form.html'
    form_class = NewsForm
    success_url = reverse_lazy('mickroservices:news')

    def get_context_data(self, **kwargs):
        context = super(NewsCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание новости'
        context['breadcrumb'] = [
            {'title': 'Новости',
             'url': reverse_lazy('mickroservices:news')},
            {'title': context['title']}
        ]
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.title, allow_unicode=True)
        self.object.seo_title = self.object.title
        homepage = Page.objects.get(url_path='/home/')
        homepage.add_child(instance=self.object)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ms='Ошибка заполнения формы'):
        print(form.errors)
        print(form.cleaned_data)
        return TemplateResponse(self.request,
                                self.template_name,
                                {'form': form,
                                 'status_ms': True,
                                 'message': ms})


class NewsEditView(UpdateView):
    template_name = 'news_form.html'
    form_class = NewsForm
    model = NewsPage
    success_url = reverse_lazy('mickroservices:news')

    def get_context_data(self, **kwargs):
        context = super(NewsEditView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирование новости'
        context['breadcrumb'] = [
            {'title': 'Новости',
             'url': reverse_lazy('mickroservices:news')},
            {'title': context['title']}
        ]
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.title, allow_unicode=True)
        self.object.seo_title = self.object.title
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ms='Ошибка заполнения формы'):
        print(form.errors)
        print(form.cleaned_data)
        return TemplateResponse(self.request,
                                self.template_name,
                                {'form': form,
                                 'status_ms': True,
                                 'message': ms})
