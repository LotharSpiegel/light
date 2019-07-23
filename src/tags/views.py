from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
# from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .models import Tag


def tag_detail(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    photos = tag.photos.all()[:20]
    context = {'tag': tag,
               'photos': photos,}
    return render(request, 'tags/detail.html', context)