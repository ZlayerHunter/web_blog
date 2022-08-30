from django.urls import re_path
from . import views as views_ac
from django.contrib.auth import views as views_dj

app_name = 'accounts'

urlpatterns = [
    # post views
    #re_path(r'^login/$', views_ac.user_login, name='login'),
    re_path(r'^login/$', views_dj.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', views_dj.LogoutView.as_view(), name='logout'),
    re_path(r'^logout-then-login/$', views_dj.logout_then_login, name='logout_then_login'),
    re_path(r'^$', views_ac.dashboard, name='dashboard'),
    re_path(r'^images/$', views_ac.images, name='images'),
    re_path(r'^password-change/$', views_dj.PasswordChangeView.as_view(), name='password_change'),
    re_path(r'^password-change/done/$', views_dj.PasswordChangeDoneView.as_view(), name='password_change_done'),
]