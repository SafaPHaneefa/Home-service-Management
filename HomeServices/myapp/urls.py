from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('error', views.error, name='error'),
    path('appointment', views.appointment, name='appointment'),
    path('contact', views.contact, name='contact'),
    path('feature', views.feature, name='feature'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('service', views.service, name='service'),
    path('team', views.team, name='team'),
    path('testimonial', views.testimonial, name='testimonial'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('register/', views.register, name='register'),
    path('userregister/', views.userregister, name='userregister'),
    path('check_availability/', views.check_availability, name='check_availability'),
    path('home/', views.home, name='home'),
    path('worker_home/', views.worker_home, name='worker_home'),
    path('login/', views.login_view, name='login'), 
    path('update/', views.update, name='update'),
    path('view_profile/', views.view_profile, name='view_profile'),
    ####################################################
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'), # Correct login view mapping

]




