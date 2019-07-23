from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import View 



def class_login_required(cls):
	if (not isinstance(cls, type) or not (issubclass(cls, View))):
		raise ImproperlyConfigured("class_login_required must be applied to subclasses of View class.")
	decorator = method_decorator(login_required)
	cls.dispatch = decorator(cls.dispatch)
	return cls