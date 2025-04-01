from django.contrib import admin

# Register your models here.
from .models import BloodDonor, BloodCamp

admin.site.register(BloodDonor)
admin.site.register(BloodCamp)
