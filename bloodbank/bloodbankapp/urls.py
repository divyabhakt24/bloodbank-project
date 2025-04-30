from django.urls import path
from . import views
from .views import bloodbank_list, bloodbank_detail, DonorRegisterView,donor_list,hospital_detail, request_blood, request_confirmation

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


    # <-- create this view if not done
]
