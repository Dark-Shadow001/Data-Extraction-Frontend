from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Contact
from datetime import datetime

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone', 'organization', 'is_staff',
                    'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'organization__organization_name', 'is_staff',
                     'is_superuser')
    fieldsets = ((None, {'fields': ('userId', 'username', 'password')}),
                 ('Personal info', {
                     'fields': ('first_name', 'last_name', 'email', 'email_validation', 'phone')}),
                 ('Organization info', {
                     'fields': ('organization',)}),
                 ('Subscribe info', {
                     'fields': ('is_subscriber', 'is_active_subscriber')}),
                 ('Permissions', {'fields': ('is_active', 'is_staff',
                                             'is_superuser', 'groups', 'user_permissions')}),
                 ('Important dates', {'fields': ('last_login', 'date_joined')})
                 )
    readonly_fields = ('userId', 'last_login', 'date_joined')
    autocomplete_fields = ('organization',)

    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        obj.updated_at = datetime.utcnow()
        obj.updated_by = request.user.username
        super().save_model(request, obj, form, change)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('contactId', 'first_name', 'last_name',
                    'email', 'phone', 'company')
    search_fields = ('contactId', 'first_name', 'last_name',
                     'email', 'phone', 'company')
    readonly_fields = ('contactId', 'created_at',)
    autocomplete_fields = ('product',)


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.unregister(Group)
