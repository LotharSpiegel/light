from django.forms import ModelForm

from .models import Snippet


class SnippetUpdateForm(ModelForm):

    class Meta:
        model = Snippet
        fields = ['title', 'language', 'code', 'description']