from django.conf.urls import url
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import LightLoginView, LightLogoutView, MemberProfileDetail, MemberProfileUpdate, \
				PublicProfileDetail, LightPasswordChangeView, LightPasswordChangeDoneView, \
				RegisterAccountView, RegisterAccountDoneView, \
				ActivateAccountView, DisableAccountView


app_name = 'accounts'


urlpatterns = [
	url(r'^login/$', LightLoginView.as_view(), 
		name='login'),
    #url(r'^logout/$', LightLogoutView.as_view(), 
    	#name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/edit/', MemberProfileUpdate.as_view(), name='profile_update'),
    url(r'^profile/(?P<slug>[\w\-]+)/$', PublicProfileDetail.as_view(), name='profile_view'),
    
    path('profile/', MemberProfileDetail.as_view(), name='profile_view'),
	url(r'^settings/password/$', LightPasswordChangeView.as_view(),
            name='password_change'),
	url(r'^settings/password/done/$', LightPasswordChangeDoneView.as_view(),
			name='password_change_done'),
	path('register/', RegisterAccountView.as_view(),
		name='register_user'),
	path('register/done/', RegisterAccountDoneView.as_view(),
		name='register_user_done'),
	url(r'^activate/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
		r'-[0-9A-Za-z]{1,20})/$',
		ActivateAccountView.as_view(),
		name='activate'),
]

# TODO: name='disable'