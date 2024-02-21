from django.urls import path
from .views import FetchData, FetchOrganisationList, FetchProductList

urlpatterns = [
    path('organization/fetchdata', FetchData.as_view(), name="fetchData"),
    path('organization/fetchogranizationlist',
         FetchOrganisationList.as_view(), name="fetchOrganizationList"),
    path('organization/fetchproductlist',
         FetchProductList.as_view(), name="fetchProductList")
]
