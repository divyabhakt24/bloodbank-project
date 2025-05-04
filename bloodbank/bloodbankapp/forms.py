from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import BloodDonor, Donation, BloodRequest
from django.utils import timezone
from datetime import date

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

class BloodDonorForm(forms.ModelForm):
    age = forms.IntegerField(
        validators=[
            MinValueValidator(18, message="Donors must be at least 18 years old"),
            MaxValueValidator(65, message="Donors must be younger than 65 years")
        ]
    )
    BLOOD_GROUP_CHOICES = [
        ('', '--- Select Blood Group ---'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = BloodDonor
        fields = ['name', 'age', 'blood_group', 'contact_number', 'email', 'address']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'blood_group': 'Blood Type',
            'contact_number': 'Phone Number'
        }


class DonationForm(forms.ModelForm):
    donation_date = forms.DateField(
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date', 'max': date.today().isoformat()})
    )
    blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES)

    class Meta:
        model = Donation
        fields = ['donor', 'blood_bank', 'blood_group', 'quantity_ml', 'donation_date']
        widgets = {
            'donor': forms.Select(attrs={'class': 'form-select'}),
            'blood_bank': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'quantity_ml': forms.NumberInput(attrs={'min': 200, 'max': 500}),
        }

    def clean_quantity_ml(self):
        quantity = self.cleaned_data['quantity_ml']
        if not 200 <= quantity <= 500:
            raise forms.ValidationError("Donation quantity must be between 200ml and 500ml")
        return quantity


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['blood_type', 'units', 'urgency', 'contact_number', 'notes']  # Removed email
        widgets = {
            'blood_type': forms.Select(attrs={'class': 'form-select'}),
            'units': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

class DonorRegistrationForm(forms.ModelForm):
    confirm_email = forms.EmailField(label="Confirm Email")
    agree_to_terms = forms.BooleanField(
        required=True,
        label="I agree to the terms and conditions"
    )

    class Meta:
        model = BloodDonor
        fields = [
            'name', 'age', 'gender', 'blood_group',
            'contact_number', 'email', 'address',
            'medical_history', 'last_donation_date'
        ]
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'last_donation_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'gender': forms.Select(choices=[
                ('M', 'Male'),
                ('F', 'Female'),
                ('O', 'Other')
            ]),
        }
        help_texts = {
            'last_donation_date': "Leave blank if never donated before"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_donation_date'].required = False

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')

        if email and confirm_email and email != confirm_email:
            self.add_error('confirm_email', "Emails do not match")

        age = cleaned_data.get('age')
        if age and age < 18:
            self.add_error('age', "Donors must be at least 18 years old")

        return cleaned_data

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')