from django.urls import path
from . import views
from .views import donor_list, blood_camp_list

urlpatterns = [
    path('login/', views.login, name='login'),
path('donate/', views.donate_view, name='donate'),

]
