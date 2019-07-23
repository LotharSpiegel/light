from django.shortcuts import get_object_or_404, redirect, render, reverse

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
    context = {
        'languages': languages,
    }
    template_name = 'snippets/languages_list.html'
    return render(request, template_name, context)

def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    context = {
        'snippet': snippet,
    }
    template_name = 'snippets/snippet_detail.html'
    return render(request, template_name, context)

def snippets_lists(request, language_slug=None):
    print('language_slug: ', language_slug)
    if language_detail is None:
        snippets = Snippet.objects.all()
    else:
        snippets = Snippet.objects.filter(language__slug=language_slug)
    context = {
        'snippets': snippets,
    }
    template_name = 'snippets/snippets_list.html'
    return render(request, template_name, context)