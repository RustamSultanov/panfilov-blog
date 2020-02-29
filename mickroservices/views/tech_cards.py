from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import ListView
from django.views.decorators.vary import vary_on_headers
from django.utils.encoding import force_text

from wagtail.admin.forms.search import SearchForm
from wagtail.admin.utils import PermissionPolicyChecker
from wagtail.core.models import Collection

from wagtail.documents.forms import get_document_form
from wagtail.documents.permissions import permission_policy

from mickroservices.models import DocumentSushi, Subjects

permission_checker = PermissionPolicyChecker(permission_policy)


class SushiDocListView(ListView):
    model = DocumentSushi
    paginate_by = 9
    context_object_name = 'documents'
    template_name = 'tech_cards.html'

    def __init__(self, *args, **kwargs):

        return super().__init__(*args, **kwargs)

    def get_documents(self):
        documents = DocumentSushi.objects.filter(doc_type=self.doc_type)
        subjects = Subjects.objects.filter(type=self.doc_type)
        if subjects:
            documents = documents.filter(sub_type=subjects[0])

        return documents

    def get_queryset(self):

        # Get documents (filtered by user permission)
        documents = self.get_documents()
        # Ordering
        ordering = None
        if 'ordering' in self.request.GET \
                and self.request.GET['ordering'] in ['title',
                                                     '-created_at',
                                                     'file_size']:
            ordering = self.request.GET['ordering']
        else:
            ordering = 'title'
        documents = documents.order_by(ordering)

        # Search
        query_string = None
        if 'q' in self.request.GET:
            form = SearchForm(self.request.GET, placeholder="Search documents")
            if form.is_valid():
                query_string = form.cleaned_data['q']
                documents = documents.search(query_string)

        return documents

    def get(self, request, *args, **kwargs):

        collections = permission_policy.collections_user_has_any_permission_for(
            request.user, ['add', 'change']
        )
        if len(collections) < 2:
            collections = None
        else:
            collections = Collection.order_for_display(collections)

        # Create response
        return super().get(request, *args, **kwargs)

    @vary_on_headers('X-Requested-With')
    def post(self, request, *args, **kwargs):
        try:
            DocumentForm = get_document_form(self.model)
        except AttributeError:
            DocumentForm = get_document_form(self.document_model)
        if not request.is_ajax():
            return HttpResponseBadRequest("Cannot POST to this view without AJAX")

        if not request.FILES:
            return HttpResponseBadRequest("Must upload a file")

        # Build a form for validation
        form = DocumentForm({
            'title': request.FILES['file'].name,
            'collection': request.POST.get('collection'),
        }, {
            'file': request.FILES['file']
        }, user=request.user)

        if form.is_valid():
            # Save it
            doc = form.save(commit=False)
            doc.doc_type = self.doc_type
            if 'sub_type' in request.POST:
                print('sub_type:',request.POST['sub_type'])
                doc.sub_type = Subjects.objects.get(pk=request.POST['sub_type'])
            doc.uploaded_by_user = request.user
            doc.file_size = doc.file.size

            # Set new document file hash
            doc.file.seek(0)
            doc._set_file_hash(doc.file.read())
            doc.file.seek(0)
            doc.save()
            print(doc, doc.sub_type)

            collections = permission_policy.collections_user_has_any_permission_for(
                request.user, ['add', 'change']
            )
            if len(collections) < 2:
                collections = None
            else:
                collections = Collection.order_for_display(collections)

            return JsonResponse({
                'success': True,
                'documents': [{'title': doc.title, 'file_size': doc.file_size} for doc in self.get_documents()],
                'collections': collections,
                'doc_id': int(doc.id),
            })
        else:
            # Validation error
            return JsonResponse({
                'success': False,
                # https://github.com/django/django/blob/stable/1.6.x/django/forms/util.py#L45
                'error_message': '\n'.join(['\n'.join([force_text(i) for i in v]) for k, v in form.errors.items()]),
            })


class TechCardsListView(SushiDocListView):
    doc_type = DocumentSushi.T_TEH_CARD

    def get_context_data(self, **kwargs):
        subjects = Subjects.objects.filter(type=self.doc_type)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Техкарты'
        context['breadcrumb'] = [{'title': context['title']}]
        context['doc_type'] = DocumentSushi.T_TEH_CARD
        context['subjects'] = subjects
        return context


class RegulationsListView(SushiDocListView):
    doc_type = DocumentSushi.T_REGULATIONS

    def get_context_data(self, **kwargs):
        subjects = Subjects.objects.filter(type=self.doc_type)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регламенты'
        context['breadcrumb'] = [{'title': context['title']}]
        context['doc_type'] = DocumentSushi.T_REGULATIONS
        context['subjects'] = subjects
        return context
