try:
	from settings.light_config import light
except ImportError:
	light = {
		'title': 'Title',
	}


def base(request):
	return {
		'light': light,
	}