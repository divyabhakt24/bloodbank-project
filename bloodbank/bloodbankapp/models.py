from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

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
