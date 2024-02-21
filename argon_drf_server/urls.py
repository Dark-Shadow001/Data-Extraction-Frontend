from django.contrib import admin
from django.urls import path, include, re_path
from user.views import render_react

admin.site.site_url = None

urlpatterns = [
    path('admin_panel/', admin.site.urls),
    path("", include("authentication.urls")),  # Auth routes - login / register
    path("", include("organization.urls")),
    path("", include("subscription.urls")),
    path("", include("user.urls")),
    re_path(r"^$", render_react),
    re_path(r"^(?:.*)/?$", render_react),
]
