from django.core.exceptions import ValidationError
from django.apps import apps

from .models import slugify


def validate_title(value):
    slug = slugify(value)
    Page = apps.get_model('contents', 'Page')
    qs = Page.objects.filter(slug=slug)
    if qs.exists():
        raise ValidationError('Page with this title already exists!')