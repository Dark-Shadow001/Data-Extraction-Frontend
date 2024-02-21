from django.contrib import admin
from .models import Campaign
from datetime import datetime

# Register your models here.


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_id', 'campaign_name', 'organization')
    search_fields = ('campaign_id', 'campaign_name',
                     'organization__organization_name')
    readonly_fields = ('campaign_id',)
    autocomplete_fields = ('organization',)

    def save_model(self, request, obj, form, change):
        obj.updated_at = datetime.utcnow()
        obj.updated_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(Campaign, CampaignAdmin)
