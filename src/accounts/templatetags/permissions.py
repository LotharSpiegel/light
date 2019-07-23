from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name)
    return group in user.groups.all()

@register.filter(name='edit_on')
def edit_on(request):
	edit_on = request.session.get('edit_on', False)
	return edit_on

@register.filter(name='editorial_on')
def editorial_on(request):
	editorial_group = Group.objects.get(name="Editorial staff")
	if editorial_group in request.user.groups.all():
		edit_on = request.session.get('edit_on', False)
		return edit_on
	return False