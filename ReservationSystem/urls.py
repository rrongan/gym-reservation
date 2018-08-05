"""ReservationSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from reservation import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^permissiondenied/$', views.permission_denied, name='permission_denied'),
    url(r'^(?P<uid>\d+)/user_reservation/$', views.user_reservation_list, name='user_reservation_list'),
    url(r'^(?P<uid>\d+)/user_reservation/create$', views.user_reservation_create, name='user_reservation_create'),
    url(r'^(?P<uid>\d+)/user_reservation/(?P<pk>\d+)/update$', views.user_reservation_update, name='user_reservation_update'),
    url(r'^(?P<uid>\d+)/user_reservation/(?P<pk>\d+)/delete', views.user_reservation_delete, name='user_reservation_delete'),
    url(r'^(?P<uid>\d+)/user_history/$', views.user_history_list, name='user_history_list'),
    url(r'^user_facility/$', views.user_facility_list, name='user_facility_list'),
    url(r'^profile/(?P<pk>\d+)/$', views.user_profile, name='user_profile'),
    url(r'^profile/(?P<pk>\d+)/update/$', views.user_profile_update, name='user_profile_update'),
    url(r'^profile/(?P<pk>\d+)/delete/$', views.user_profile_delete, name='user_profile_delete'),
    url(r'^profile/password/$', views.change_password, name='change_password'),
    url(r'^reservation/$', views.reservation_list, name='reservation_list'),
    url(r'^reservation/create/$', views.reservation_create, name='reservation_create'),
    url(r'^reservation/(?P<pk>\d+)/update/$', views.reservation_update, name='reservation_update'),
    url(r'^reservation/(?P<pk>\d+)/delete/$', views.reservation_delete, name='reservation_delete'),
    url(r'^facility/$', views.facility_list, name='facility_list'),
    url(r'^facility/create/$', views.facility_create, name='facility_create'),
    url(r'^facility/(?P<pk>\d+)/update/$', views.facility_update, name='facility_update'),
    url(r'^facility/(?P<pk>\d+)/delete/$', views.facility_delete, name='facility_delete'),
    url(r'^user/$', views.user_list, name='user_list'),
    url(r'^user/create/$', views.user_create, name='user_create'),
    url(r'^user/(?P<pk>\d+)/update/$', views.user_update, name='user_update'),
    url(r'^user/(?P<pk>\d+)/delete/$', views.user_delete, name='user_delete'),
]
