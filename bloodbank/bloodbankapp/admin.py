from django.contrib import admin

# Register your models here.
from .models import BloodDonor, BloodCamp

from django.contrib import admin
from .models import BloodDonor, BloodCamp


class BloodDonorInline(admin.TabularInline):
    model = BloodCamp.donors.through
    extra = 1


class BloodDonorAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'blood_group', 'contact_number', 'email', 'units_donated', 'last_donation_date']
    search_fields = ['name', 'blood_group', 'email']
    list_filter = ['blood_group', 'last_donation_date']
    exclude = ('camps_attended',)


class BloodCampAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'date', 'organizer']
    search_fields = ['name', 'location', 'organizer']
    list_filter = ['date', 'location']
    inlines = [BloodDonorInline]
    autocomplete_fields = ['donors']


# Register models with customization
admin.site.register(BloodDonor, BloodDonorAdmin)
admin.site.register(BloodCamp, BloodCampAdmin)

