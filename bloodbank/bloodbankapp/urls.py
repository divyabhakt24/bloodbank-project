from django.urls import path
from . import views
from .views import bloodbank_list, bloodbank_detail, DonorRegisterView,donor_list,hospital_detail, request_blood, request_confirmation, my_blood_requests, CustomLoginView, register
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('donate/', views.donate, name='donate'),
    path('blood-donations/', views.blood_donations, name='blood_donations'),
    path('donors/', views.donor_list, name='donors_list'),
    path('blood-camps/', views.blood_camp_list, name='blood_camps'),
    path('blood-banks/', views.blood_bank_list, name='blood_banks'),  # <-- creat this view if not done
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('hospitals/<int:pk>/', hospital_detail, name='hospital_detail'),
    path('bloodbanks/', bloodbank_list, name='bloodbank_list'),
    path('bloodbanks/<int:pk>/', bloodbank_detail, name='bloodbank_detail'),
    path('donors/register/', DonorRegisterView.as_view(), name='donor_register'),
    path('request-blood/<int:hospital_id>/', request_blood, name='request_blood'),
    path('request-confirmation/', request_confirmation, name='request_confirmation'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('donors/', donor_list, name='donor_list'),
    path('donors/<int:pk>/', views.donor_detail, name='donor_detail'),
    path('donors/<int:pk>/edit/', views.donor_edit, name='donor_edit'),
    path('donors/<int:pk>/request/', views.request_donor, name='request_donor'),
    path('nearby-camps/', views.nearby_camps_view, name='nearby_camps'),
    path('hospitals/map/', views.hospital_map, name='hospital-map'),
    path('request/confirmation/<int:request_id>/', views.request_confirmation, name='request_confirmation'),
    path('request/confirmation/<int:request_id>/', views.request_confirmation, name='request_confirmation'),
    path('my-requests/', my_blood_requests, name='my_blood_requests'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('request-blood/hospital/<int:hospital_id>/', request_blood, name='request_blood_hospital'),
    path('request-blood/bank/<int:bank_id>/', views.request_blood, name='request_blood_bank'),
    path('request-blood/', views.request_blood, name='request_blood_general'),

    # Password reset URLs
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # <-- create this view if not done
]