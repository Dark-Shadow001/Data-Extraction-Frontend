from django.contrib import admin
from .models import OTP
try:
    from rest_framework.authtoken.models import TokenProxy as DRFToken
except ImportError:
    from rest_framework.authtoken.models import Token as DRFToken
    
# Register your models here.

# admin.site.register(OTP) # OTP table in admin not registered
admin.site.unregister(DRFToken)