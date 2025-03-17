from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import verify_otp_view, resend_otp_view
from .views import manage_bookings
from django.conf.urls.static import static
from django.conf import settings
from .views import delete_service
from .views import servicelist, service_details
from .views import manage_subservice, edit_subservice, delete_subservice

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
    path('worker_registration/', views.worker_registration, name='worker_registration'),
    path('registration_success/', views.registration_success, name='worker_registration_success'),
    path('userregister/', views.userregister, name='userregister'),
    path('check_availability/', views.check_availability, name='check_availability'),
    path('home/', views.home, name='home'),
    path('worker_home/', views.worker_home, name='worker_home'),
    path('login/', views.login_view, name='login'), 
    path('update/', views.update, name='update'),
    path('view_profile/', views.view_profile, name='view_profile'), 
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-workers/', views.manage_workers, name='manage_workers'),
    path('update_worker/', views.update_worker, name='update_worker'),
    path('add_service/', views.add_service, name='add_service'),
    path('add_worker/', views.add_worker, name='add_worker'),
    path('add_worker/<int:worker_id>/', views.add_worker, name='add_worker'),   # New URL for adding a worker
    path('logout/', views.logout, name='logout'),
    path('logout_view/',views.logout_view, name='logout_view'),
    path('booking_view/',views.booking_view,name='bookings'),
    path('booking/', views.booking, name='booking'),
    path('verify_otp/', verify_otp_view, name='verify_otp'),
    path('resend_otp/', resend_otp_view, name='resend_otp'),
    path('deactivate_user/', views.deactivate_user, name='deactivate_user'),
    path('deactivate_worker/', views.deactivate_worker, name='deactivate_worker'),
    path('manage_bookings/', views.manage_bookings, name='manage_bookings'),  
    path('submit-feedback/', views.submit_feedback, name='feedback_form'),
    path('search-work/',views.search_work, name='search_work'),
    path('approve_worker/', views.approve_worker, name='approve_worker'),
    path('manage_services/', views.manage_services, name='manage_services'),
    path('service/delete/<int:service_id>/',views. delete_service, name='delete_service'),
    path('service/edit_service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
####################################################
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'), # Correct login view mapping
    path('add-announcement/', views.add_announcement, name='add_announcement'),
    path('view-announcements/', views.view_announcements, name='view_announcements'),
    path('delete-announcement/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
    path('certificate/<str:filename>/', views.certificate_view, name='certificate_view'),
    path('resume/<str:filename>/', views.resume_view, name='resume_view'),
    path('profile_image/<str:filename>/', views.profile_image_view, name='profile_image_view'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('worker_bookings/', views.worker_bookings, name='worker_bookings'),
    path('chatbot/', views.chatbot_response, name='chatbot_response'),  # Add this line
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('accept_booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('request_start_timer/<int:booking_id>/', views.request_start_timer, name='request_start_timer'),
    path('request_stop_timer/<int:booking_id>/', views.request_stop_timer, name='request_stop_timer'),
    path('get_timer_start/<int:booking_id>/', views.get_timer_start, name='get_timer_start'),
    path('start_timer/<int:booking_id>/', views.start_timer, name='start_timer'),
    path('accept_timer_start/<int:booking_id>/', views.accept_timer_start, name='accept_timer_start'),
    path('reject_timer_start/<int:booking_id>/', views.reject_timer_start, name='reject_timer_start'),
    path('confirm_stop_timer/<int:booking_id>/', views.confirm_stop_timer, name='confirm_stop_timer'),
    path('reject_stop_timer/<int:booking_id>/', views.reject_stop_timer, name='reject_stop_timer'),
    path('send_bill/<int:booking_id>/', views.send_bill, name='send_bill'),
    path('payment_history/', views.payment_history, name='payment_history'),
    path('user_payment_history/', views.user_payment_history, name='user_payment_history'),
    path('initiate_payment/<int:payment_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),
    path('api/detect-service', views.detect_service, name='detect_service'),
    path('smart_detection/', views.smart_view, name='smart_view'),
    path('add-service-list/', views.add_service_list, name='admin_add_service_list'),
    path('service/<int:service_id>/', views.service_details, name='service_details'),
    path('services/', views.servicelist, name='service_list'),
    path('manage_subservice/', views.manage_subservice, name='manage_subservice'),
    path('edit_subservice/<int:sub_service_id>/', views.edit_subservice, name='edit_subservice'),
    path('delete_subservice/<int:sub_service_id>/', views.delete_subservice, name='delete_subservice'),# Add this line for the servicelist view
    path('get_booking_status/<int:booking_id>/', views.get_booking_status, name='get_booking_status'),
    path('api/start-location-sharing/', views.start_location_sharing, name='start_location_sharing'),
    path('api/worker-location/<int:worker_id>/<int:booking_id>/', views.get_worker_location, name='get_worker_location'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





