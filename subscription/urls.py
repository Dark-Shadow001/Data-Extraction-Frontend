from django.urls import path
from .views import FetchSubscriptionData

urlpatterns = [
    path('subscription/fetchsubscriptiondata', FetchSubscriptionData.as_view(), name="fetchSubscriptionData"),
]
