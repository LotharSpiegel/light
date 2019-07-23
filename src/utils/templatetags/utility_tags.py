from __future__ import unicode_literals
import re
from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_str
import urllib

register = template.Library()

### FILTERS ###

media_tags_regex = re.compile(
    r"<figure[\S\s]+?</figure>|"
    r"<object[\S\s]+?</object>|"
    r"<video[\S\s]+?</video>|"
    r"<audio[\S\s]+?</audio>|"
    r"<iframe[\S\s]+?</iframe>|"
    r"<(img|embed)[^>]+>",
    re.MULTILINE
)

@register.filter
def first_media(content):
    """
    :param content:
    :return: the first image or flash file from the html content
    """
    m = media_tags_regex.search(content)
    media_tag = ""
    if m:
        media_tag = m.group()
    return mark_safe(media_tag)

# use like this:
# {% load utility_tags %}
# {{ object.content|first_media }}

### TAGS ###

@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url

@register.simple_tag(takes_context=True)
def modify_query(
        context, *params_to_remove, **params_to_change):
    """ Renders a link with modified current query parameters
    """
    query_params = []
    for key, value_list in context["request"].GET._iterlists():
        if not key in params_to_remove:
            # don't add key-value pairs for
            # params_to_change
            if key in params_to_change:
                query_params.append(
                    (key, params_to_change[key])
                )

                params_to_change.pop(key)
            else:
                # leave existing parameters as they were
                # if not mentioned in the params_to_change
                for value in value_list:
                    query_params.append((key, value))

    # attach new params
    for key, value in params_to_change.items():
        query_params.append((key, value))
    query_string = context["request"].path
    if len(query_params):
        query_string +="?%s" % urllib.urlencode([
            (key, force_str(value))
            for (key, value) in query_params if value
        ]).replace("&", "&amp;")
    return query_string