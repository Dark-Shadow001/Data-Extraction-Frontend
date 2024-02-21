from django.contrib import admin
from .models import Organization, Product
from datetime import datetime

# Register your models here.


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_id', 'organization_name', 'website', 'contact_email',
                    'country', 'subscription_start_date', 'subscription_end_date', 'is_subscrition_active')
    search_fields = ('organization_id', 'organization_name', 'website', 'contact_email',
                     'country', 'subscription_start_date', 'subscription_end_date', 'is_subscrition_active')
    readonly_fields = ('organization_id',
                       'subscription_start_date', 'subscription_end_date', 'is_subscrition_active')

    def save_model(self, request, obj, form, change):
        obj.updated_at = datetime.utcnow()
        obj.updated_by = request.user.username
        super().save_model(request, obj, form, change)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name',
                    'product_desc', 'start_date', 'end_date')
    search_fields = ('product_id', 'product_name',
                     'product_desc', 'start_date', 'end_date')
    readonly_fields = ('product_id',)

    def save_model(self, request, obj, form, change):
        obj.updated_at = datetime.utcnow()
        obj.updated_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Product, ProductAdmin)
