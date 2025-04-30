from django.contrib import admin
from .models import (
    BloodDonor, BloodCamp, BloodRequest, Donation,
    Hospital,BloodBank
)
from .admin_utis import ExportCsvMixin
from django.utils.html import format_html


class BloodDonorInline(admin.TabularInline):
    model = BloodCamp.donors.through
    extra = 1

class BloodDonorAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['name', 'age', 'blood_group', 'contact_number', 'email', 'units_donated', 'last_donation_date']
    search_fields = ['name', 'blood_group', 'email']
    list_filter = ['blood_group', 'last_donation_date']
    exclude = ('camps_attended',)
    actions = ['export_as_csv']

class BloodCampAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['name', 'location', 'date', 'organizer']
    search_fields = ['name', 'location', 'organizer']
    list_filter = ['date', 'location']
    inlines = [BloodDonorInline]
    autocomplete_fields = ['donors']
    actions = ['export_as_csv']

class DonationAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['donor', 'blood_bank', 'blood_group', 'quantity_ml', 'date']
    list_filter = ['blood_group', 'blood_bank', 'date']
    search_fields = ['donor__name', 'blood_group']
    autocomplete_fields = ['donor', 'blood_bank']
    date_hierarchy = 'date'
    readonly_fields = ['date']
    actions = ['export_as_csv']

class BloodRequestAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['hospital', 'blood_group', 'quantity_ml', 'request_date', 'status', 'fulfilled_by']
    list_filter = ['blood_group', 'status', 'request_date']
    search_fields = ['hospital__name']
    autocomplete_fields = ['hospital', 'fulfilled_by']
    date_hierarchy = 'request_date'
    readonly_fields = ['status']
    actions = ['export_as_csv']

    def colored_status(self, obj):
        color = 'green' if obj.status == 'Fulfilled' else 'orange'
        return format_html(f'<b style="color:{color}">{obj.status}</b>')

    colored_status.short_description = 'Status'
    list_display = ['hospital', 'blood_group', 'quantity_ml', 'request_date', 'colored_status', 'fulfilled_by']


class BloodBankAdmin(admin.ModelAdmin,ExportCsvMixin):
    search_fields = ['name', 'location']
    actions = ['export_as_csv']

class HospitalAdmin(admin.ModelAdmin,ExportCsvMixin):
    search_fields = ['name', 'location']
    actions = ['export_as_csv']


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'hospital_type', 'city', 'phone')
    list_filter = ('hospital_type',)
    search_fields = ('name', 'address')

    def city(self, obj):
        return obj.address.split(',')[-1] if obj.address else "Unknown"

# Registering all models with respective admin configs
admin.site.register(BloodDonor, BloodDonorAdmin)
admin.site.register(BloodCamp, BloodCampAdmin)

admin.site.register(BloodBank, BloodBankAdmin)
admin.site.register(BloodRequest, BloodRequestAdmin)
admin.site.register(Donation, DonationAdmin)


