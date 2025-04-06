from django import forms
from .models import BloodDonor

class BloodDonorForm(forms.ModelForm):
    class Meta:
        model = BloodDonor
        fields = ['name', 'age', 'blood_group', 'contact_number', 'email', 'address']
