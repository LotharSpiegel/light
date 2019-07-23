
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from .views import *

app_name = 'tags'

urlpatterns = [
    path('<tag_slug>', tag_detail, name='tag_detail'),
]
