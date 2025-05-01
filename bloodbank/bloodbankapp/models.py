from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone



class BloodDonor(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-')
    ]

    name = models.CharField(max_length=100)
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
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)  # For URLs
    location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.CharField(max_length=150)
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?\d{10,15}$', 'Enter a valid phone number')]
    )
    description = models.TextField(blank=True, null=True)
    donors = models.ManyToManyField(BloodDonor, related_name='camps_attended', blank=True)  # Track donors

    def __str__(self):
        return f"{self.name} - {self.date}"


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


class BloodBank(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)  # Add this
    longitude = models.FloatField(null=True, blank=True)

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
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5)
    quantity_ml = models.PositiveIntegerField()
    request_date = models.DateField(auto_now_add=True)
    status_choices = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Fulfilled', 'Fulfilled')
    ]
    URGENCY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical')
    ]

    required_by = models.DateField(default=timezone.now() + timezone.timedelta(days=3))
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='normal')
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')
    fulfilled_by = models.ForeignKey(BloodBank, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.blood_group} - {self.quantity_ml}ml to {self.hospital.name}"

class BloodDonationCamp(models.Model):
        name = models.CharField(max_length=255)
        address = models.TextField()
        latitude = models.FloatField()
        longitude = models.FloatField()
        date = models.DateField()