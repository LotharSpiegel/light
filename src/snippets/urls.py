
from django.urls import include, path

from .views import *

app_name = 'snippets'

urlpatterns = [
    path('<int:snippet_id>/edit/', SnippetUpdateView.as_view(), name='snippet_edit'),
    path('<int:snippet_id>/', snippet_detail, name='snippet_detail'),
    path('new/', SnippetCreateView.as_view(), name='snippet_create'),
    path('lang/<slug:language_slug>/', snippets_list, name='snippets_list_lang'),
    path('', snippets_list, name='snippets_list'),
]