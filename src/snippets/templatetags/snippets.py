from django import template

from ..models import Snippet

register = template.Library()


@register.simple_tag(name='snippet_is_editable')
def snippet_is_editable(snippet, user):
    return snippet.is_editable(user)

@register.simple_tag(name='code_snippet_by_id')
def code_snippet_by_id(id):
    snippet = Snippet.objects.get(id=id)
    # if not found, include ... snippet not found image
    return snippet.render()