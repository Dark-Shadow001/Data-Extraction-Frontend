from django.contrib import admin
from .models import Subscription
from datetime import datetime
from organization.models import Organization

# Register your models here.


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscription_id', 'subscription_name', 'organization',
                    'start_date', 'end_date')
    search_fields = ('subscription_id', 'subscription_name', 'organization__organization_name',
                     'start_date', 'end_date')
    readonly_fields = ('subscription_id',)
    autocomplete_fields = ('organization',)

    def save_model(self, request, obj, form, change):
        orgId = obj.organization_id
        org = Organization.objects.filter(organization_id=orgId)[0]
        org.is_subscrition_active = True
        org.subscription_start_date = obj.start_date
        org.subscription_end_date = obj.end_date
        org.save()
        obj.updated_at = datetime.utcnow()
        obj.updated_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(Subscription, SubscriptionAdmin)
