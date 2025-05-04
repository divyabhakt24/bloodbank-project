from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Sum
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import BloodDonor, BloodCamp, BloodBank, Hospital, BloodRequest, UserProfile
from .forms import DonationForm, DonorRegistrationForm, BloodRequestForm
from datetime import date
from bloodbank.utils.geocoding import get_coordinates
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bloodbank.utils.osm_utils import fetch_osm_hospitals
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def home(request):
    return render(request, 'home.html')


def login(request):
    return HttpResponse("<form><h2>Login Form</h2></form>")


def blood_donations(request):
    donors_count = BloodDonor.objects.count()
    blood_units = BloodDonor.objects.aggregate(total_units=Sum('units_donated'))['total_units'] or 0
    upcoming_camps = BloodCamp.objects.filter(date__gte=date.today()).order_by('date')[:3]

    context = {
        'donors_count': donors_count,
        'blood_units': blood_units,
        'upcoming_camps': upcoming_camps
    }
    return render(request, 'blood_donations.html', context)


def create_donor(request):
    if request.method == "POST":
        try:
            donor = BloodDonor.objects.create(
                name=request.POST.get('name', ''),
                age=request.POST.get('age', 18),
                blood_group=request.POST.get('blood_group', 'O+'),
                contact_number=request.POST.get('contact_number', ''),
                email=request.POST.get('email', ''),
                address=request.POST.get('address', ''),
                units_donated=request.POST.get('units_donated', 0)
            )
            return JsonResponse({
                "message": "Donor Created Successfully",
                "donor_id": donor.id
            })
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)
    return JsonResponse({
        "error": "Invalid request method"
    }, status=405)


def donor_list(request):
    search_term = request.GET.get('search', '')
    blood_group = request.GET.get('blood_group', '')

    donors = BloodDonor.objects.all()

    if search_term:
        donors = donors.filter(
            Q(name__icontains=search_term) |
            Q(contact_number__icontains=search_term) |
            Q(email__icontains=search_term)
        )

    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    paginator = Paginator(donors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'donor_list.html', {
        'donors': page_obj,
        'search_term': search_term,
        'blood_group': blood_group
    })


def blood_camp_list(request):
    camps = BloodCamp.objects.all()
    return render(request, 'blood_camp_list.html', {'camps': camps})


def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save()
            return redirect('thank_you')
    else:
        form = DonationForm()
    return render(request, 'donate.html', {'form': form})


def blood_bank_list(request):
    bloodbanks = BloodBank.objects.all()
    return render(request, 'bloodbank_list.html', {'bloodbanks': bloodbanks})


def hospital_list(request):
    hospitals = Hospital.objects.all()
    return render(request, 'hospital_list.html', {'hospitals': hospitals})


def bloodbank_list(request):
    bloodbanks = BloodBank.objects.all()
    search_term = request.GET.get('search', '')
    blood_group = request.GET.get('blood_group', '')

    if search_term:
        bloodbanks = bloodbanks.filter(
            Q(name__icontains=search_term) |
            Q(city__icontains=search_term) |
            Q(state__icontains=search_term)
        )

    if blood_group:
        bloodbanks = bloodbanks.filter(available_groups__name=blood_group)

    # Move pagination outside the search_term condition
    paginator = Paginator(bloodbanks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bloodbank_list.html', {
        'bloodbanks': page_obj,
        'search_term': search_term,
        'blood_group': blood_group
    })


def bloodbank_detail(request, pk):
    bank = get_object_or_404(BloodBank, id=pk)
    return render(request, 'bloodbank_detail.html', {'bank': bank})


class DonorRegisterView(CreateView):
    model = BloodDonor
    form_class = DonorRegistrationForm
    template_name = 'donor_register.html'
    success_url = reverse_lazy('donor_list')

def hospital_detail(request, pk):
    hospital = get_object_or_404(Hospital, id=pk)
    return render(request, 'hospital_detail.html', {'hospital': hospital})


@login_required
def request_blood(request, bank_id):
    bloodbank = get_object_or_404(BloodBank, id=bank_id)

    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.bloodbank = bloodbank
            blood_request.status = 'pending'
            blood_request.save()
            messages.success(request, 'Your blood request has been submitted successfully!')
            return redirect('request_confirmation', request_id=blood_request.id)
    else:
        initial_data = {}
        if hasattr(request.user, 'profile'):
            initial_data = {
                'contact_number': request.user.profile.phone_number,
                'email': request.user.email,
            }
        else:
            initial_data = {
                'email': request.user.email,
            }
        form = BloodRequestForm(initial=initial_data)

    context = {
        'bloodbank': bloodbank,
        'form': form,
        'title': f'Blood Request - {bloodbank.name}'
    }
    return render(request, 'blood_request_form.html', context)


def request_confirmation(request, request_id):
    """
    Shows confirmation page after successful submission
    """
    blood_request = get_object_or_404(BloodRequest, id=request_id, requester=request.user)
    return render(request, '/request_confirmation.html', {
        'request': blood_request
    })


# Helper function for sending notifications
def send_blood_request_notification(blood_request):
    """
    Sends email/other notifications about the blood request
    """
    # Implementation depends on your email setup
    pass


def request_confirmation(request):
    return render(request, 'request_confirmation.html')

def donor_detail(request, pk):
    donor = get_object_or_404(BloodDonor, pk=pk)
    return render(request, 'donor_detail.html', {'donor': donor})

def donor_edit(request, pk):
    donor = get_object_or_404(BloodDonor, pk=pk)
    # Add your edit form logic here
    return render(request, 'donor_edit.html', {'donor': donor})

def request_donor(request, pk):
    donor = get_object_or_404(BloodDonor, pk=pk)
    # Add your request logic here
    return render(request, 'request_donor.html', {'donor': donor})

from django.shortcuts import render
from .models import BloodDonationCamp
import folium
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    # Calculate the great-circle distance between two points
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in kilometers

def nearby_camps_view(request):
    user_lat = float(request.GET.get('lat', 0))
    user_lon = float(request.GET.get('lon', 0))
    radius_km = 10  # Define the radius to search within

    # Filter camps within the specified radius
    camps = []
    for camp in BloodDonationCamp.objects.all():
        distance = haversine_distance(user_lat, user_lon, camp.latitude, camp.longitude)
        if distance <= radius_km:
            camps.append((camp, distance))

    # Create a Folium map centered at the user's location
    m = folium.Map(location=[user_lat, user_lon], zoom_start=13)

    # Add a marker for the user's location
    folium.Marker(
        [user_lat, user_lon],
        tooltip='Your Location',
        icon=folium.Icon(color='blue')
    ).add_to(m)

    # Add markers for each nearby camp
    for camp, distance in camps:
        folium.Marker(
            [camp.latitude, camp.longitude],
            tooltip=f"{camp.name} ({distance:.2f} km)",
            popup=camp.address,
            icon=folium.Icon(color='red')
        ).add_to(m)

    # Render the map as HTML
    map_html = m._repr_html_()

    return render(request, 'nearby_camps.html', {'map': map_html})


def thank_you(request):
    return render(request, 'thank_you.html')  # Make sure you have this template

def add_bloodbank(request):
    if request.method == "POST":
        address = request.POST.get("address")
        lat, lng = get_coordinates(address)
        if lat and lng:
            BloodBank.objects.create(
                name=request.POST.get("name"),
                address=address,
                latitude=lat,
                longitude=lng
            )


@api_view(['GET'])
def nearby_hospitals(request):
    location = request.GET.get('location', 'India')
    cache_key = f'hospitals_{location}'

    # Check cache first
    hospitals = cache.get(cache_key)

    if not hospitals:
        # Fetch from OSM if not in cache
        hospitals = fetch_osm_hospitals(location)
        # Cache for 1 hour
        cache.set(cache_key, hospitals, 3600)

    return Response({
        'location': location,
        'count': len(hospitals),
        'hospitals': hospitals[:20]  # Return first 20 for demo
    })


def hospital_map(request):
    hospitals = Hospital.objects.all().order_by('name')

    # Pagination for very large datasets
    paginator = Paginator(hospitals, 500)  # Show 500 hospitals per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'hospitals/map.html', {
        'hospitals': page_obj,
        'page_obj': page_obj  # For pagination controls
    })

def request_confirmation(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    context = {
        'blood_request': blood_request,
        'title': 'Request Confirmation'
    }
    return render(request, 'request_confirmation.html', context)

@login_required
# views.py (optional filtering)
def my_blood_requests(request):
    bank_id = None
    if hasattr(request.user, 'userprofile') and request.user.userprofile.bank:
        bank_id = request.user.userprofile.bank.id

    context = {
        'blood_requests': BloodRequest.objects.filter(requester=request.user),
        'bank_id': bank_id,
    }
    return render(request, 'my_blood_requests.html', context)

from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')