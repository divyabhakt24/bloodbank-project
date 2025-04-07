from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('donate/', views.donate, name='donate'),
    path('blood-donations/', views.blood_donations, name='blood_donations'),
    path('donors/', views.donor_list, name='donors_list'),
    path('blood-camps/', views.blood_camp_list, name='blood_camps'),
    path('blood-banks/', views.blood_bank_list, name='blood_banks'),  # <-- create this view if not done
    path('hospitals/', views.hospital_list, name='hospital_list'),    # <-- create this view if not done
]
