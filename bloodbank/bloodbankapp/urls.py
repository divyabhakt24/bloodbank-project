from django.urls import path
from . import views
from .views import bloodbank_list, bloodbank_detail, DonorRegisterView,donor_list,hospital_detail, request_blood, request_confirmation, my_blood_requests, CustomLoginView, register,initiate_cross_city_donation, cross_city_donation_status, confirm_donation, manage_cross_city_transfers, mark_as_transferred, mark_as_received,register_patient, patient_dashboard
from django.contrib.auth import views as auth_views
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


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
    path('my-requests/', my_blood_requests, name='my_blood_requests'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('request-blood/hospital/<int:hospital_id>/', request_blood, name='request_blood_hospital'),
    path('request-blood/bank/<int:bank_id>/', views.request_blood, name='request_blood_bank'),
    path('request-blood/', views.request_blood, name='request_blood'),
    path('offer-donation/', views.create_donation_offer, name='create_offer'),
    path('main/request/<int:request_id>/find-donors/', views.find_donors, name='find_donors'),
    path('request-blood/<int:bank_id>/', views.request_blood, name='request_blood_with_bank'),
    # For general blood requests (without specific bank)
    path('request-blood/', views.request_blood, name='request_blood'),
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),

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
    path('request-blood/', views.create_blood_request, name='create_request'),
    path('request/<int:request_id>/find-donors/', views.find_donors, name='find_donors'),
    path('offer-donation/', views.create_donation_offer, name='create_offer'),
    path('match/<int:match_id>/confirm/', views.confirm_match, name='confirm_match'),
    path('match/<int:match_id>/complete/', views.complete_match, name='complete_match'),
    path('my-matches/', views.my_matches, name='my_matches'),
    path('about/', views.about, name='about'),
    path('organize-camp/', views.organize_camp, name='organize_camp'),
    path('camp-confirmation/', views.camp_confirmation, name='camp_confirmation'),



    # ... intercity donations ...
    path('cross-city-donation/', initiate_cross_city_donation, name='initiate_cross_city_donation'),
    path('cross-city-donation/<int:donation_id>/', cross_city_donation_status, name='cross_city_donation_status'),
    path('cross-city-donation/<int:donation_id>/confirm/', confirm_donation, name='confirm_donation'),
    path('admin/cross-city-donations/', manage_cross_city_transfers, name='manage_cross_city_transfers'),
    path('admin/cross-city-donations/<int:donation_id>/transferred/', mark_as_transferred, name='mark_as_transferred'),
    path('admin/cross-city-donations/<int:donation_id>/received/', mark_as_received, name='mark_as_received'),
    path('cross-city-donation/<int:donation_id>/check-status/', cross_city_donation_status, name='check_donation_status'),
    # <-- create this view if not done
    path('patient/register/', register_patient, name='register_patient'),
    path('patient/dashboard/', login_required(patient_dashboard), name='patient_dashboard'),
]