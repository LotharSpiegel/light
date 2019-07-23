# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.contrib.auth import get_user, get_user_model, logout # login as auth_login
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, \
									PasswordChangeDoneView
from django.contrib.messages import error, success
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
#from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
#from content.views import page_view
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, TemplateView, DetailView, UpdateView

from .decorators import class_login_required
from .forms import RegisterNewUserForm
from .models import MemberProfile
from .utils import MailContextViewMixin, MemberProfileGetObjectMixin


# try:
# 	from content.views import ContentPageView
# except ImportError:
# 	pass

try:
	from light.breadcrumbs import base_breadcrumbs
except ImportError:
	def make_breadcrumbs_links(breadcrumb_titles):
		return [(title, '#') for title in breadcrumb_titles]


class BasePageViewMixin:
	template_name = 'page.html'


class LightLoginView(BasePageViewMixin, LoginView):
	extra_context = {
		'page': 'accounts/login.html',
		'title': 'Login',
		'breadcrumbs': make_breadcrumbs_links([
						'Home',
						'Login']),
	}


class LightLogoutView(BasePageViewMixin, LogoutView):
	extra_context = {
		'page': 'accounts/logout.html',
		'title': 'Logout',
		'breadcrumbs': make_breadcrumbs_links([
						'Home',
						'Logout']),
	}


class LightPasswordChangeView(BasePageViewMixin, PasswordChangeView):
	extra_context = {
		'page': 'accounts/password_change.html',
		'title': 'Change Password',
		'breadcrumbs': make_breadcrumbs_links([
						'Home',
						'Change Password']),
	}


class LightPasswordChangeDoneView(BasePageViewMixin, PasswordChangeDoneView):
	extra_context = {
		'page': 'accounts/password_change_done.html',
		'title': 'Password change done',
		'breadcrumbs': make_breadcrumbs_links([
						'Home',
						'Password change done']),
	}


@class_login_required
class MemberProfileDetail(BasePageViewMixin, MemberProfileGetObjectMixin, DetailView):
	model = MemberProfile

	extra_context = {
		'page': 'accounts/profile_detail.html',
		'title': 'Member Profile',
		'breadcrumbs': make_breadcrumbs_links([
						'Home',
						'Member Profile']),
	}


@class_login_required
class MemberProfileUpdate(BasePageViewMixin, MemberProfileGetObjectMixin, UpdateView):
	model = MemberProfile

	fields = ('about', 'website',)

	extra_context = {
		'page': 'accounts/profile_update.html',
		'title': 'Edit Member Profile',
		'breadcrumbs': make_breadcrumbs_links([
						'Home',
						'Edit Member Profile']),
	}


class PublicProfileDetail(BasePageViewMixin, DetailView):
	model = MemberProfile

	extra_context = {
		'page': 'accounts/profile_detail.html',
		'title': 'Member Profile',
		'breadcrumbs': make_breadcrumbs_links([
						'Home',
						'Member Profile']),
	}

	# def get_object(self, queryset=None):
	# 	current_user = get_user(self.request)
	# 	return current_user.profile

	def get_context_object_name(self, obj):
		return 'profile'


# TemplateView.as_view(extra_context={'title': 'Custom Title'})

class RegisterAccountView(BasePageViewMixin, MailContextViewMixin, View):
	form_class = RegisterNewUserForm
	success_url = reverse_lazy(
		'accounts:register_user_done')
	extra_context = {
		'page': 'accounts/user_register.html',
		'title': 'Password change done',
		'breadcrumbs': make_breadcrumbs_links([
						'Home',
						'Register new member account']),
	}

	def get_context_data(self, **kwargs):
		#context = super().get_context_data(**kwargs)
		context = self.extra_context
		#context.update(self.extra_context)
		return context

	#@method_decorator(csrf_protect)
	def get(self, request):
		#context = self.get_context_data()
		context = self.get_context_data()
		form = self.form_class()
		self.extra_context.update({'form': form})
		return TemplateResponse(
			request, self.template_name, context=context)

	@method_decorator(csrf_protect)
	@method_decorator(sensitive_post_parameters(
		'password1', 'password2'))
	def post(self, request):
		bound_form = self.form_class(request.POST)
		if bound_form.is_valid():
			bound_form.save(**self.get_save_kwargs(request))
			if bound_form.mail_sent:
				return redirect(self.success_url)
			else:
				errs = (
					bound_form.non_field_errors())
				for err in errs:
					error(request, err)
				# TODO: redirect to email resend
		context = self.get_context_data()
		context.update({'form': bound_form})
		return TemplateResponse(
			request, self.template_name, context=context)


class RegisterAccountDoneView(BasePageViewMixin, TemplateView):
	extra_context = {
		'page': 'accounts/user_register_done.html',
		'title': 'New user registered',
		'breadcrumbs': make_breadcrumbs_links([
						'Home',
						'New user registered']),
	}


class ActivateAccountView(View):
	success_url = reverse_lazy('accounts:login')
	template_name = 'accounts/user_activate.html'


	@method_decorator(never_cache)
	def get(self, request, uidb64, token):
		User = get_user_model()
		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError,
			OverflowError, User.DoesNotExist):
			user = None
		if (user is not None and token_generator.check_token(user, token)):
			user.is_active = True
			user.save()
			success(
				request,
				'User Activated! You may now login.')
			return redirect(self.success_url)

		else:
			return TemplateResponse(request,
				self.template_name)


class DisableAccountView:
	pass

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     context = {'form': form}
#     return render(request, 'accounts/signup.html', context=context)

# @login_required
# def settings(request):
#     if request.method =='POST':
#         form = UserSettingsForm(request.POST)
#         if form.is_valid():
#             #daten speichern
#             return redirect('home')
#     else:
#         form = UserSettingsForm()
#     context = {'form': form}
#     return render(request, 'accounts/user_settings.html', context=context)

# class UserUpdateView(UpdateView):
#     model = User
#     fields = ('first_name',
#               'last_name',
#               'email',)
#     template_name = 'accounts/my_account.html'
#     success_url = '/settings/account'#reverse('my_account')

#     def get_object(self):
#         return self.request.user