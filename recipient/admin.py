from django.contrib import admin
from .models import Recipient, BloodRequest

@admin.action(description="Mark selected as Approved")
def approve_requests(modeladmin, request, queryset):
    queryset.update(status='Approved')

@admin.action(description="Mark selected as Rejected")
def reject_requests(modeladmin, request, queryset):
    queryset.update(status='Rejected')

class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'units', 'city', 'status')
    list_filter = ('status', 'blood_group', 'city')
    actions = [approve_requests, reject_requests]

admin.site.register(Recipient)
admin.site.register(BloodRequest, BloodRequestAdmin)