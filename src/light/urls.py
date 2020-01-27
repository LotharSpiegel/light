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
from django.views.generic.base import RedirectView


# def homepage(request):
#     return redirect
    #return HttpResponse('homepage')

def contact(request):
    return HttpResponse('contact')

def about(request):
    return HttpResponse('about')

from contents.views import view_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('members/', include('accounts.urls', namespace='accounts')),
    path('pages/', include('contents.urls', namespace='contents')),
    path('snippets/', include('snippets.urls', namespace='snippets')),

    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('', RedirectView.as_view(url='pages/index', permanent=False), name='homepage'),
]
