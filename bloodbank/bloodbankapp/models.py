from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date  # Add this import at the top of models.py


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.state}"

class BloodDonor(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-')
    ]

    name = models.CharField(max_length=100,null=True, blank=True)
    donor_city = models.CharField(max_length=100,null=True, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(65)])  # Ensure valid age
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)  # Use predefined choices
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?\d{10,15}$', 'Enter a valid phone number')]
    )
    email = models.EmailField(unique=True, null=True, blank=True)
    address = models.TextField()
    units_donated = models.PositiveIntegerField(default=0)
    last_donation_date = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    medical_history = models.TextField(blank=True)


    def __str__(self):
        return f"{self.name} ({self.blood_group})"

class BloodCamp(models.Model):
    """Unified blood camp model (includes donation camps and other events)"""
    CAMP_TYPES = [
        ('donation', 'Blood Donation Camp'),
        ('awareness', 'Awareness Program'),
        ('mixed', 'Mixed Event'),
    ]

    name = models.CharField(max_length=255,null=True)
    camp_type = models.CharField(max_length=20, choices=CAMP_TYPES, default='donation',null=True)
    organizer = models.CharField(max_length=255,null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.TextField(null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    contact_number = models.CharField(max_length=15,null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    donors = models.ManyToManyField(BloodDonor, blank=True, null=True)


    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"



from django.core.validators import URLValidator, EmailValidator
from django.db import models


class Hospital(models.Model):
    HOSPITAL_TYPES = [
        ('general', 'General Hospital'),
        ('specialty', 'Specialty Hospital'),
        ('teaching', 'Teaching Hospital'),
        ('clinic', 'Clinic'),
        ('government', 'Government Hospital'),
        ('private', 'Private Hospital'),
    ]

    osm_id = models.BigIntegerField(unique=True, null=True, blank=True, help_text="OpenStreetMap ID")
    name = models.CharField(max_length=255, null=True, blank=True)
    hospital_type = models.CharField(
        max_length=50,
        choices=HOSPITAL_TYPES,
        default='general',
        null=True
    )
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text="Include country code if available"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        validators=[EmailValidator()]
    )
    website = models.URLField(
        blank=True,
        null=True,
        validators=[URLValidator()],
        help_text="Full website URL including https://"
    )

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Hospitals'

    def __str__(self):
        return f"{self.name} ({self.get_hospital_type_display()})"

    @property
    def coordinates(self):
        return (self.latitude, self.longitude)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'address'],
                name='unique_hospital_name_address'
            )
        ]

class BloodBank(models.Model):
    name = models.CharField(max_length=150,null=True, blank=True)
    state = models.TextField(max_length=20,null=True,blank=True)
    district = models.TextField(max_length=30,null=True,blank=True)
    address = models.TextField(null=True, blank=True)
    pincode = models.BigIntegerField (blank=True,null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.BigIntegerField(blank=True,null=True)
    email = models.EmailField(
        blank=True,
        null=True,
        validators=[EmailValidator()]
    )
    website = models.URLField(
        blank=True,
        null=True,
        validators=[URLValidator()],
        help_text="Full website URL including https://"
    )
    category = models.TextField(blank=True,null=True)
    blood_component_available = models.TextField(blank=True,null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name



class Donation(models.Model):
    donor = models.ForeignKey(BloodDonor, on_delete=models.CASCADE)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    blood_group = models.CharField(max_length=5)
    quantity_ml = models.PositiveIntegerField()

    def __str__(self):
        return f"Donation by {self.donor.name} on {self.date}"


class BloodRequest(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    URGENCY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, null=True)
    units = models.PositiveIntegerField(null=True)
    urgency = models.CharField(max_length=10, choices=URGENCY_LEVELS, default='medium', null=True)
    contact_number = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True, blank=True)  # Add this line
    request_date = models.DateTimeField(auto_now_add=True, null=True)
    hospital = models.CharField(max_length=100, null=True)
    fulfilled = models.BooleanField(default=False, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    hospital_name = models.CharField(max_length=100, null=True, blank=True)
    patient_name = models.CharField(max_length=100, null=True, blank=True)
    units_required = models.PositiveIntegerField(null=True, blank=True)
    can_accept_from_other_cities = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    required_by = models.DateField(null=True, blank=True)

    # Add status field

    def __str__(self):
        return f"{self.blood_type} request ({self.units} units)"


class UserProfile(models.Model):
    name = models.CharField(max_length=255,null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank = models.ForeignKey('BloodBank', on_delete=models.SET_NULL, null=True, blank=True)
    hospital = models.ForeignKey('Hospital', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user.username

class CampRegistration(models.Model):
    """Tracks donor registrations for camps"""
    donor = models.ForeignKey(BloodDonor, on_delete=models.CASCADE)
    camp = models.ForeignKey(BloodCamp, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    donation_made = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('donor', 'camp')

    def __str__(self):
        return f"{self.donor} at {self.camp}"





class DonationOffer(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('matched', 'Matched'),
        ('donated', 'Donated'),
    ]

    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    available_date = models.DateField()
    contact_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    can_travel = models.BooleanField(default=False)
    max_travel_distance = models.PositiveIntegerField(default=0)  # in km
    created_at = models.DateTimeField(auto_now_add=True)


class BloodDonationMatch(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE)
    donation_offer = models.ForeignKey(DonationOffer, on_delete=models.CASCADE)
    matched_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    matched_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)


class BloodDonationCamp(models.Model):
    name = models.CharField(max_length=200,null =True)
    organizer = models.CharField(max_length=100,null =True)
    location = models.CharField(max_length=200,null =True)
    date = models.DateField(null =True)
    start_time = models.TimeField(null =True)
    end_time = models.TimeField(null =True)
    expected_donors = models.PositiveIntegerField(null =True)
    contact_email = models.EmailField(null =True)
    contact_phone = models.CharField(max_length=15,null =True)
    additional_notes = models.TextField(blank=True,null =True)
    created_at = models.DateTimeField(default=timezone.now,null =True)
    is_approved = models.BooleanField(default=False,null =True)

    def __str__(self):
        return f"{self.name} on {self.date}"

class BloodInventory(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, null=True, blank=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    units_available = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('hospital', 'blood_type'), ('blood_bank', 'blood_type'))


# Patients
class Patient(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('U', 'Prefer not to say')
    ]

    # Basic Information
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)

    # Contact Information
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?\d{10,15}$', 'Enter a valid phone number')])
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Address Information
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')

    # Medical Information
    primary_physician = models.CharField(max_length=255, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)

    # Hospital Information
    preferred_hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_blood_bank = models.ForeignKey(BloodBank, on_delete=models.SET_NULL, null=True, blank=True)

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_relation = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.blood_type})"

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['last_name', 'first_name']


# Intercity Blood Donation
class CrossCityDonation(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('donated', 'Donated'),
        ('transferred', 'Transferred'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]

    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cross_city_donations',null=True, blank=True)
    donor_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='donor_city',null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='cross_city_donations',null=True, blank=True)
    patient_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='patient_city',null=True, blank=True)
    blood_type = models.CharField(max_length=3, choices=BloodDonor.BLOOD_GROUPS,null=True, blank=True)
    units = models.PositiveIntegerField(null=True, blank=True)
    donor_blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='donor_blood_bank',null=True, blank=True)
    patient_blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='patient_blood_bank',null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='initiated',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    donation_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(null=True, blank=True)
    state_name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return f"Donation from {self.donor_city} to {self.patient_city} ({self.blood_type})"

    # models.py
    def update_inventory(self):
        if not self.blood_type:  # Add validation
            raise ValueError("Blood type is required for inventory updates")

        if self.status == 'donated':
            # Ensure donor_blood_bank exists
            if not self.donor_blood_bank:
                raise ValueError("Donor blood bank is required")

            donor_inventory, created = BloodInventory.objects.get_or_create(
                blood_bank=self.donor_blood_bank,
                blood_type=self.blood_type,
                defaults={'units_available': 0}
            )
            donor_inventory.units_available += self.units
            donor_inventory.save()

        elif self.status == 'received':
            # Ensure both banks exist
            if not self.donor_blood_bank or not self.patient_blood_bank:
                raise ValueError("Both blood banks are required for transfer")

            # Get donor inventory (must exist)
            try:
                donor_inventory = BloodInventory.objects.get(
                    blood_bank=self.donor_blood_bank,
                    blood_type=self.blood_type
                )
                donor_inventory.units_available -= self.units
                donor_inventory.save()
            except BloodInventory.DoesNotExist:
                raise ValueError("Donor inventory not found")

            # Get or create patient inventory
            patient_inventory, created = BloodInventory.objects.get_or_create(
                blood_bank=self.patient_blood_bank,
                blood_type=self.blood_type,
                defaults={'units_available': 0}
            )
            patient_inventory.units_available += self.units
            patient_inventory.save()

    def clean(self):
        if not self.blood_type:
            raise ValidationError("Blood type is required")

        if self.status == 'donated' and not self.donor_blood_bank:
            raise ValidationError("Donor blood bank is required for donated status")

        if self.status == 'received' and not self.patient_blood_bank:
            raise ValidationError("Patient blood bank is required for received status")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run model validation
        super().save(*args, **kwargs)


