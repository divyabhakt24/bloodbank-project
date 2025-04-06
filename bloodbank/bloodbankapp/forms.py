from django import forms
from .models import BloodDonor

class BloodDonorForm(forms.ModelForm):
    class Meta:
        model = BloodDonor
        fields = ['name', 'age', 'blood_group', 'contact_number', 'email', 'address']
from .models import Donation, BloodRequest

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor', 'blood_bank', 'blood_group', 'quantity_ml']

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['hospital', 'blood_group', 'quantity_ml']