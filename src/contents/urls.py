
from django.urls import include, path

from contents.views import (PageCreateView, PageDeleteView,
    PageUpdateView, view_page,
    pages_index, preview_page) #, PublishedPageView, NotPublishedYetPageView


app_name = 'contents'


urlpatterns = [
    #path('edit/pages/<slug:page_slug>', ),
    path('new/', PageCreateView.as_view(), name='create_page'),
    # path('pages/<slug:slug>/not_published', NotPublishedYetPageView.as_view(), name='view_page_not_published'),
    # path('pages/<slug:slug>', PublishedPageView.as_view(), name='view_page'),
    path('<slug:page_slug>/preview/', preview_page, name='preview_page'),
    path('<slug:page_slug>/edit/', PageUpdateView.as_view(), name='edit_page'),
    path('<slug:page_slug>/delete/', PageDeleteView.as_view(), name='delete_page'),
    #path(', name='default_homepage'),
    path('<slug:page_slug>/', view_page, name='view_page'),
    path('', pages_index, name='pages_index'),
]