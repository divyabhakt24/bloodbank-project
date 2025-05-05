from django.contrib import admin
from .models import (
    BloodDonor, BloodCamp, BloodRequest, Donation,
    Hospital,BloodBank,BloodDonationCamp
)
from .admin_utis import ExportCsvMixin
from django.utils.html import format_html
import requests



class BloodDonorInline(admin.TabularInline):
    model = BloodCamp.donors.through
    extra = 1

class BloodDonorAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['name', 'age', 'blood_group', 'contact_number', 'email', 'units_donated', 'last_donation_date']
    search_fields = ['name', 'blood_group', 'email']
    list_filter = ['blood_group', 'last_donation_date']
    exclude = ('camps_attended',)
    actions = ['export_as_csv']

class BloodCampAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['name', 'get_location', 'get_duration', 'city', 'organizer']
    search_fields = ['name', 'organizer', 'city__name']
    list_filter = ['start_date', 'city']
    inlines = [BloodDonorInline]
    autocomplete_fields = ['donors']
    actions = ['export_as_csv']

    def get_location(self, obj):
        return f"{obj.address}, {obj.city}"
    get_location.short_description = 'Location'

    def get_duration(self, obj):
        return f"{obj.start_date} to {obj.end_date}"
    get_duration.short_description = 'Duration'

class DonationAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['donor', 'blood_bank', 'blood_group', 'quantity_ml', 'date']
    list_filter = ['blood_group', 'blood_bank', 'date']
    search_fields = ['donor__name', 'blood_group']
    autocomplete_fields = ['donor', 'blood_bank']
    date_hierarchy = 'date'
    readonly_fields = ['date']
    actions = ['export_as_csv']

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'blood_type', 'units', 'urgency', 'requester', 'hospital', 'request_date', 'fulfilled')
    list_filter = ('blood_type', 'urgency', 'fulfilled', 'request_date')
    search_fields = ('hospital', 'requester__username', 'contact_number')
    date_hierarchy = 'request_date'


class BloodBankAdmin(admin.ModelAdmin,ExportCsvMixin):
    search_fields = ['name', 'location']
    actions = ['export_as_csv']

class HospitalAdmin(admin.ModelAdmin,ExportCsvMixin):
    search_fields = ['name', 'location']
    actions = ['export_as_csv']


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'hospital_type', 'address', 'state', 'phone', 'map_link')
    list_filter = ('hospital_type', 'state')
    search_fields = ('name', 'address', 'district', 'pincode')
    list_per_page = 50
    actions = ['fetch_osm_data']
    readonly_fields = ('last_updated', 'osm_id')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'hospital_type')
        }),
        ('Location', {
            'fields': ('address', 'state', 'district', 'pincode',
                       ('latitude', 'longitude'), 'osm_id')
        }),
        ('Contact', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Metadata', {
            'fields': ('last_updated',)
        })
    )

    def city(self, obj):
        """Extract city from address"""
        if obj.district:
            return obj.district
        if obj.address:
            parts = [p.strip() for p in obj.address.split(',')]
            return parts[-2] if len(parts) > 1 else parts[-1]
        return "Unknown"

    city.short_description = 'City/District'

    def phone_display(self, obj):
        """Formatted phone number with country code"""
        if not obj.phone:
            return "-"
        phone = obj.phone
        return f"+91 {phone[:5]} {phone[5:]}" if len(phone) == 10 else phone

    phone_display.short_description = 'Phone'

    def map_link(self, obj):
        """Google Maps link if coordinates exist"""
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank">View Map</a>', url)
        return "-"

    map_link.short_description = 'Map'

    def fetch_osm_data(self, request, queryset):
        """Admin action to fetch missing data from OSM"""
        from django.contrib import messages
        for hospital in queryset.filter(osm_id__isnull=False):
            try:
                response = requests.get(
                    f"https://api.openstreetmap.org/api/0.6/node/{hospital.osm_id}",
                    timeout=5
                )
                if response.status_code == 200:
                    # Add your OSM data parsing logic here
                    pass
            except requests.RequestException as e:
                messages.warning(request, f"Failed to fetch OSM data: {str(e)}")
        self.message_user(request, f"Updated {queryset.count()} hospitals")

    fetch_osm_data.short_description = "Fetch OSM data"

    def get_urls(self):
        """Add custom admin views"""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-osm/', self.admin_site.admin_view(self.import_osm_view), name='import_osm'),
        ]
        return custom_urls + urls

    def import_osm_view(self, request):
        """Custom view for bulk OSM import"""
        if request.method == 'POST':
            # Handle form submission
            return redirect('..')
        from django.shortcuts import render
        context = self.admin_site.each_context(request)
        return render(request, 'admin/hospitals/import_osm.html', context)

# Registering all models with respective admin configs
admin.site.register(BloodDonor, BloodDonorAdmin)
admin.site.register(BloodCamp, BloodCampAdmin)
admin.site.register(BloodBank, BloodBankAdmin)
admin.site.register(Donation, DonationAdmin)

@admin.register(BloodDonationCamp)
class BloodDonationCampAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'organizer', 'is_approved')
    list_filter = ('is_approved', 'date')
    search_fields = ('name', 'location', 'organizer')