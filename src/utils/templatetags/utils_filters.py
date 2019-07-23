from django.template.defaultfilters import register 

@register.filter(name='lookup')
def lookup(dict, index):
	if index in dict:
		return dict[index]
	return None

@register.filter(name='skip_last')
def skip_last(a_list):
	if a_list:
		return a_list[:-1]
	return None

@register.filter(name='last_item')
def last_item(a_list):
	if a_list:
		return a_list[-1]
	return None

@register.filter(name='item')
def item(a_list, index):
	if a_list:
		return a_list[index]
	return None