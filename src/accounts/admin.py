from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import MemberProfile

User = get_user_model()

class MemberProfileInline(admin.StackedInline):
	model = MemberProfile
	can_delete = False
	verbose_name_plural = 'Member Profiles'
	fk_name = 'user'

	# list_display = ('slug', 'website')
	# search_fields = ('slug', 'website', 'about')
	# list_filter = ('slug',)
	# #prepopulated_fields = {'slug': ('name',)}


class CustomUserAdmin(UserAdmin):
	inlines = (MemberProfileInline, )

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

	#add_form = RegisterNewUserForm
	#form = UserAdminSettingsForm
	model = User
	list_display = ['username',
	                'email',
	                #'is_editorial_staff',
	                #'password1',
	                #'password2']
	                ]
	#fieldsets = UserAdmin.fieldsets + (
	#    (None, {'fields': ('is_editorial_staff',)}),
	#)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)