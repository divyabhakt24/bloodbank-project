from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import BloodDonor, BloodCamp
from .forms import DonationForm


def home(request):
    return render(request, 'home.html')

def login(request):
    return HttpResponse("<form> <h2>hi</h2></form>")

def blood_donations(request):
    donors_count = BloodDonor.objects.count()
    blood_units = BloodDonor.objects.aggregate(total_units=Sum('units_donated'))['total_units']
    upcoming_camps = BloodCamp.objects.all()[:3]

    context = {
        'donors_count': donors_count,
        'blood_units': blood_units,
        'upcoming_camps': upcoming_camps
    }
    return render(request, 'blood_donations.html', context)

def create_donor(request):
    if request.method == "POST":
        donor = BloodDonor.objects.create(
            name="John Doe",
            age=28,
            blood_group="O+",
            contact_number="+911234567890",
            email="johndoe@example.com",
            address="123 Street, City",
            units_donated=2
        )
        return JsonResponse({"message": "Donor Created", "donor_id": donor.id})

def donor_list(request):
    donors = BloodDonor.objects.all()  # Fetch all donors
    return render(request, 'donor_list.html', {'donors': donors})

def blood_camp_list(request):
    camps = BloodCamp.objects.all()  # Fetch all blood camps
    return render(request, 'blood_camp_list.html')

def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')  # Or wherever you want to redirect
    else:
        form = DonationForm()
    return render(request, 'donate.html', {'form': form})

def blood_bank_list(request):
    return render(request, 'blood_camp_list.html')
  # create this HTML file

def hospital_list(request):
    return render(request, 'hospital_list.html')  # create this HTML file
