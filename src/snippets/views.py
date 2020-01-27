from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from contents.utils import build_breadcrumbs
from .forms import SnippetUpdateForm
from .models import Language, Snippet


def language_detail(request, language_slug):
    language = get_object_or_404(Language, slug=language_slug)
    context = {
        'language': language,
    }
    template_name = 'snippets/language_detail.html'
    return render(request, template_name, context)

def languages_list(request):
    languages = Language.objects.all()
    parents = [('Index', reverse('homepage')),]
    context = {
        'languages': languages,
        'breadcrumbs': build_breadcrumbs('Languages', reverse('snippets:languages_list'), parents),
    }
    template_name = 'snippets/languages_list.html'
    return render(request, template_name, context)

def get_render_context(snippet, request, include_breadcrumbs=True):
    context = {
        'snippet': snippet,
        'snippet_is_editable': snippet.is_editable(request.user),
    }
    if include_breadcrumbs:
        context['breadcrumbs'] = snippet.get_breadcrumbs()
    return context

def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    context = get_render_context(
        snippet=snippet, request=request, include_breadcrumbs=True)
    template_name = 'snippets/snippet_detail.html'
    return render(request, template_name, context)

# def snippet_create(request):
#     template_name = 'snippets/snippet_create.html'
#     if request.method == 'POST':
#         form =
#     else:

class SnippetUpdateView(UpdateView):
    model = Snippet
    # fields = ['title', 'language', 'code', 'description']
    context_object_name = 'snippet'
    form_class = SnippetUpdateForm
    template_name = 'snippets/edit/snippet_edit.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Snippet, pk=self.kwargs['snippet_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context

    def get_breadcrumbs(self):
        parents = [
            ('Snippets', reverse_lazy('snippets:snippets_list')),
            ('Index', reverse_lazy('homepage')),
        ]
        breadcrumbs = build_breadcrumbs('Edit Snippet',
            reverse_lazy('snippets:snippet_edit', kwargs={'id': self.object.id}),
            parents)
        return breadcrumbs

    def get_success_url(self):
        return self.object.get_absolute_url()


class SnippetCreateView(CreateView):
    model = Snippet
    # fields = ['title', 'language', 'code', 'description']
    context_object_name = 'snippet'
    form_class = SnippetUpdateForm
    template_name = 'snippets/edit/snippet_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     print('kwargs:', kwargs)
    #     kwargs['author'] = self.request.user
    #     #     kwargs['instance'] = Symbol()
    #     # kwargs['instance'].creator = self.request.user
    #     return kwargs

    def get_breadcrumbs(self):
        parents = [
            ('Snippets', reverse_lazy('snippets:snippets_list')),
            ('Index', reverse_lazy('homepage')),
        ]
        breadcrumbs = build_breadcrumbs('Create Snippet',
            reverse_lazy('snippets:snippet_create'),
            parents)
        return breadcrumbs

    def get_success_url(self):
        return self.object.get_absolute_url()


def snippets_list(request, language_slug=None):

    if language_slug is None:
        print('all snippets')
        snippets = Snippet.objects.all()
    else:
        print('language_slug: ', language_slug)
        snippets = Snippet.objects.filter(language__slug=language_slug)
    parents = [('Index', reverse('homepage')),]
    context = {
        'snippets': snippets,
        'breadcrumbs': build_breadcrumbs('Snippets', reverse('snippets:snippets_list'), parents),
    }
    template_name = 'snippets/snippets_list.html'
    return render(request, template_name, context)