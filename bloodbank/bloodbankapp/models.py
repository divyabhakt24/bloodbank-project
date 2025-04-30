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

class Hospital(models.Model):
    osm_id = models.BigIntegerField(unique=True, null=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    hospital_type = models.CharField(max_length=50, default='general')
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitals'

    def __str__(self):
        return f"{self.name} ({self.hospital_type})"

    @property
    def coordinates(self):
        return (self.latitude, self.longitude)


class BloodBank(models.Model):
    name = models.CharField(max_length=100)
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