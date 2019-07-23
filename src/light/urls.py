"""light URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def homepage(request):
    return HttpResponse('homepage')

def contact(request):
    return HttpResponse('contact')

def about(request):
    return HttpResponse('about')

from contents.views import PageCreateView, view_page, PageUpdateView#, PublishedPageView, NotPublishedYetPageView

urlpatterns = [
    # includes:
    path('admin/', admin.site.urls),
    path('members/', include('accounts.urls', namespace='accounts')),
    #path('edit/pages/<slug:page_slug>', ),
    path('new_page/', PageCreateView.as_view(), name='create_page'),
    # path('pages/<slug:slug>/not_published', NotPublishedYetPageView.as_view(), name='view_page_not_published'),
    # path('pages/<slug:slug>', PublishedPageView.as_view(), name='view_page'),
    path('pages/<slug:slug>/edit', PageUpdateView.as_view(), name='edit_page'),
    path('pages/<slug:slug>/', view_page, name='view_page'),

    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('', homepage, name='homepage'),
]
