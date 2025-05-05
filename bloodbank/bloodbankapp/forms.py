from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import BloodDonor, Donation, BloodRequest,DonationOffer, BloodDonationCamp
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


from django import forms
from .models import BloodRequest


class BloodRequestForm(forms.ModelForm):
    required_by = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = BloodRequest
        fields = [
            'patient_name',
            'blood_type',
            'units_required',
            'required_by',
            'urgency',
            'contact_number',
            'email',
            'hospital_name',
            'city',
            'can_accept_from_other_cities',
            'notes'
        ]
        widgets = {
            'required_by': forms.DateInput(attrs={'type': 'date'}),
            'can_accept_from_other_cities': forms.CheckboxInput(),
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


from django import forms
from .models import BloodRequest, DonationOffer, City
from django.core.exceptions import ValidationError


class BloodRequestForm(forms.ModelForm):
    required_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = BloodRequest
        fields = ['patient_name', 'blood_type', 'units_required',
                  'hospital_name', 'city', 'required_date', 'contact_number',
                  'can_accept_from_other_cities']
        widgets = {
            'can_accept_from_other_cities': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DonationOfferForm(forms.ModelForm):
    available_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = DonationOffer
        fields = ['blood_type', 'city', 'available_date',
                  'contact_number', 'can_travel', 'max_travel_distance']
        widgets = {
            'can_travel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        can_travel = cleaned_data.get('can_travel')
        max_travel_distance = cleaned_data.get('max_travel_distance')

        if can_travel and not max_travel_distance:
            raise ValidationError("Please specify how far you can travel")
        return cleaned_data


class DonationOfferForm(forms.ModelForm):
    class Meta:
        model = DonationOffer
        fields = ['blood_type', 'city', 'available_date', 'contact_number', 'can_travel', 'max_travel_distance']

        widgets = {
            'available_date': forms.DateInput(attrs={'type': 'date'}),
            'max_travel_distance': forms.NumberInput(attrs={'min': 0}),
        }


class BloodDonationCampForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[MinValueValidator(date.today())]
    )
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = BloodDonationCamp
        fields = [
            'name', 'organizer', 'location', 'date',
            'start_time', 'end_time', 'expected_donors',
            'contact_email', 'contact_phone', 'additional_notes'
        ]

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be later than start time.")
        return cleaned_data