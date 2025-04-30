from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Sum
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import BloodDonor, BloodCamp, BloodBank, Hospital
from .forms import DonationForm, DonorRegistrationForm, BloodRequestForm
from datetime import date


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


def request_blood(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)

    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.hospital = hospital
            blood_request.save()
            return redirect('request_confirmation')
    else:
        form = BloodRequestForm()

    return render(request, 'request_blood.html', {
        'hospital': hospital,
        'form': form
    })

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

def thank_you(request):
    return render(request, 'thank_you.html')