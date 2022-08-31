from django.urls import re_path
from . import views as views_ac
from django.contrib.auth import views as views_dj
from django.urls import reverse_lazy

app_name = 'accounts'

urlpatterns = [
    # post views
    #re_path(r'^login/$', views_ac.user_login, name='login'),
    re_path(r'^login/$', views_dj.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', views_dj.LogoutView.as_view(), name='logout'),
    re_path(r'^logout-then-login/$', views_dj.logout_then_login, name='logout_then_login'),
    re_path(r'^$', views_ac.dashboard, name='dashboard'),
    re_path(r'^images/$', views_ac.images, name='images'),
    re_path(r'^password-change/done/$', views_dj.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"),
            name='password_change_done'),    
    re_path(r'^password-change/$', views_dj.PasswordChangeView.as_view(
                                                                      template_name="registration/password_change_form.html",
                                                                      success_url = reverse_lazy("accounts:password_change_done")
                                                                      ), 
            name='password_change'),

    re_path(r'^password-reset/complete/$', views_dj.PasswordResetCompleteView.as_view(
                                                                                     template_name="registration/password_reset_complete.html"),
            name='password_reset_complete'),
    re_path(r'^password-reset/done/$', views_dj.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), 
            name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', views_dj.PasswordResetConfirmView.as_view(
                                                                                                                        template_name="registration/password_reset_confirm.html", 
                                                                                                                        success_url = reverse_lazy("accounts:password_reset_complete")),
            name='password_reset_confirm'),
    re_path(r'^password-reset/$', views_dj.PasswordResetView.as_view(
                                                                    template_name="registration/password_reset_form.html",
                                                                    email_template_name = "registration/password_reset_email.html",
                                                                    success_url=reverse_lazy("accounts:password_reset_done"),
                                                                    ),
            name='password_reset'),
    re_path(r'^register/$', views_ac.register, name='register'),        
]