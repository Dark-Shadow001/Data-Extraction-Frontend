from django.urls import path
from .views import FetchUserDetails, UpdateUserDetail, AddContactDetails

urlpatterns = [
    path('user/fetchuserdetails', FetchUserDetails.as_view(), name="fetchuserdetails"),
    path('user/updateuserdetails', UpdateUserDetail.as_view(), name="updateuserdetails"),
    path('addContactdetails', AddContactDetails.as_view(), name="updateuserdetails"),
]

